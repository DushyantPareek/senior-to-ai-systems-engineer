import asyncio
import json

from app.retrieval.retriever import retrieve


EVAL_FILE = "data/evaluation/retrieval_eval.json"


async def evaluate():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        test_cases = json.load(file)

    passed = 0

    for test_case in test_cases:
        question = test_case["question"]
        expected_document = test_case["expected_document"]

        results = await retrieve(question)

        retrieved_documents = {
            result["document_id"]
            for result in results
        }

        if expected_document is None:
            success = len(results) == 0
        else:
            success = expected_document in retrieved_documents

        if success:
            passed += 1

        status = "PASS" if success else "FAIL"

        print(f"\n[{status}] {question}")
        print(f"Expected: {expected_document}")
        print(f"Retrieved: {sorted(retrieved_documents)}")

    total = len(test_cases)

    print("\n------------------------------")
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {passed / total:.2%}")


if __name__ == "__main__":
    asyncio.run(evaluate())