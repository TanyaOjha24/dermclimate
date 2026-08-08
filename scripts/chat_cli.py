from dotenv import load_dotenv

from bootstrap.application import create_dermclimate_service


def main() -> None:
    load_dotenv()

    dermclimate = create_dermclimate_service()

    print("=" * 70)
    print("DermClimate CLI")
    print("=" * 70)
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() == "exit":
            print("\nGoodbye!")
            break

        try:
            result = dermclimate.process_message(
                user_message=user_message,
            )

            print("\nDermClimate:\n")

            if result.response:
                print(result.response)
            else:
                print(result.message)

            print()

        except Exception:
            import traceback

            print("\nFULL TRACEBACK:\n")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()