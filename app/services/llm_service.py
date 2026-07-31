import httpx
import json
import time


OLLAMA_URL = "http://localhost:11434/api/generate"


async def ask_llm(question: str) -> str:
    payload = {
        "model": "qwen3:4b",
        "prompt": question,
        "stream": False,
        "think": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        result = response.json()

    return result["response"]


import json
import time

import httpx


OLLAMA_URL = "http://localhost:11434/api/generate"


async def stream_llm(question: str):
    payload = {
        "model": "qwen3:4b",
        "prompt": question,
        "stream": True,
        "think": False,
        "options": {
            "num_predict": 300
        }
    }

    request_start = time.perf_counter()

    raw_ttft = None
    final_answer_ttft = None

    thinking = True
    buffer = ""

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json=payload
        ) as response:

            response.raise_for_status()

            async for line in response.aiter_lines():

                if not line:
                    continue

                data = json.loads(line)

                # Capture first raw output from the model
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
                        f"{data.get('done_reason')}"
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

                    break

                chunk = data.get("response", "")

                if not chunk:
                    continue

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
