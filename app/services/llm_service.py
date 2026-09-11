import httpx
import json
import time
from app.config import settings
from app.prompts.prompts import (
    SYSTEM_PROMPT,
    build_prompt
)

class LLMServiceError(Exception):
    pass


class LLMConnectionError(LLMServiceError):
    pass


class LLMTimeoutError(LLMServiceError):
    pass


class LLMResponseError(LLMServiceError):
    pass

OLLAMA_GENERATE_URL = f"{settings.ollama_url}/api/generate"


async def ask_llm(question: str, 
    context: str = "",
    system_prompt: str = SYSTEM_PROMPT
) -> str:

    prompt = build_prompt(
    question=question,
    context=context
)

    payload = {
        "model": "qwen3:4b",
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {
            "num_predict": 500
        }
    }

    try:

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                OLLAMA_GENERATE_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

        answer = result.get("response")

        if not answer:
            raise LLMResponseError(
                "LLM returned an empty response"
            )

        return answer

    except httpx.ConnectError as exc:

        raise LLMConnectionError(
            "Unable to connect to Ollama"
        ) from exc

    except httpx.ReadTimeout as exc:

        raise LLMTimeoutError(
            "LLM request timed out"
        ) from exc

    except httpx.HTTPStatusError as exc:

        raise LLMResponseError(
            f"Ollama returned HTTP "
            f"{exc.response.status_code}"
        ) from exc


async def stream_llm(question: str):
    payload = {
        "model": "qwen3:4b",
        "prompt": question,
        "stream": True,
        "think": False,
        "options": {
            "num_predict": 500
        }
    }

    request_start = time.perf_counter()

    raw_ttft = None
    final_answer_ttft = None

    thinking = True
    buffer = ""
    response_received = False

    try:

        async with httpx.AsyncClient(
            timeout=None
        ) as client:

            async with client.stream(
                "POST",
                OLLAMA_GENERATE_URL,
                json=payload
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():

                    if not line:
                        continue

                    data = json.loads(line)

                    # Capture first raw output
                    if (
                        raw_ttft is None
                        and data.get("response", "")
                    ):
                        raw_ttft = (
                            time.perf_counter()
                            - request_start
                        )

                    # Final Ollama response
                    if data.get("done"):

                        total_time = (
                            time.perf_counter()
                            - request_start
                        )

                        done_reason = data.get(
                            "done_reason"
                        )

                        print("\n[LLM Metrics]")

                        print(
                            f"Raw TTFT: "
                            f"{raw_ttft:.2f}s"
                            if raw_ttft is not None
                            else "Raw TTFT: N/A"
                        )

                        print(
                            f"Final Answer TTFT: "
                            f"{final_answer_ttft:.2f}s"
                            if final_answer_ttft is not None
                            else "Final Answer TTFT: N/A"
                        )

                        print(
                            f"Total time: "
                            f"{total_time:.2f}s"
                        )

                        print(
                            f"Output tokens: "
                            f"{data.get('eval_count')}"
                        )

                        print(
                            f"Done reason: "
                            f"{done_reason}"
                        )

                        if (
                            data.get("eval_duration")
                            and data.get("eval_count")
                        ):
                            tokens_per_second = (
                                data["eval_count"]
                                / (
                                    data["eval_duration"]
                                    / 1_000_000_000
                                )
                            )

                            print(
                                f"Tokens/sec: "
                                f"{tokens_per_second:.2f}"
                            )

                        # Token limit reached
                        if done_reason == "length":
                            yield (
                                "\n\n"
                                "[Response truncated: "
                                "the model reached its "
                                "token limit.]"
                            )
                        elif (
                            done_reason == "stop"
                            and not response_received
                        ):
                            yield (
                                "\n\n"
                                "[LLM error: "
                                "Ollama completed without "
                                "returning an answer.]"
                            )

                        break

                    chunk = data.get(
                        "response",
                        ""
                    )

                    if not chunk:
                        continue

                    response_received = True

                    # Add incoming text to buffer
                    buffer += chunk

                    # -----------------------------
                    # THINKING PHASE
                    # -----------------------------
                    if thinking:

                        if "</think>" not in buffer:
                            continue

                        # Remove everything before </think>
                        _, final_text = buffer.split(
                            "</think>",
                            1
                        )

                        thinking = False
                        buffer = ""

                        if final_text:

                            if final_answer_ttft is None:
                                final_answer_ttft = (
                                    time.perf_counter()
                                    - request_start
                                )

                            yield final_text

                    # -----------------------------
                    # FINAL ANSWER PHASE
                    # -----------------------------
                    else:

                        if final_answer_ttft is None:
                            final_answer_ttft = (
                                time.perf_counter()
                                - request_start
                            )

                        yield chunk

    except httpx.ConnectError:

        print(
            "[LLM Error] Unable to connect to Ollama"
        )

        yield (
            "\n\n"
            "[LLM connection error: "
            "Ollama is unavailable.]"
        )

    except httpx.ReadTimeout:

        print(
            "[LLM Error] Ollama request timed out"
        )

        yield (
            "\n\n"
            "[LLM timeout: "
            "the request took too long.]"
        )

    except httpx.HTTPStatusError as exc:

        print(
            "[LLM Error] Ollama returned HTTP "
            f"{exc.response.status_code}"
        )

        yield (
            "\n\n"
            "[LLM error: "
            "Ollama returned an HTTP error.]"
        )

    except json.JSONDecodeError:

        print(
            "[LLM Error] Invalid JSON received "
            "from Ollama"
        )

        yield (
            "\n\n"
            "[LLM error: "
            "received an invalid response.]"
        )