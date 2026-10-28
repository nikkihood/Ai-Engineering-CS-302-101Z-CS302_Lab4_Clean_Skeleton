# Dependency Rule: Frameworks and drivers invoke controllers and display adapter-produced view models.

from transcript_requester.frameworks_drivers.composition_root import (
    request_transcript_controller,
)


def main() -> None:
    source_url = input("Enter source URL: ").strip()
    view_model = request_transcript_controller.handle({"source_url": source_url})
    print(view_model)


if __name__ == "__main__":
    main()
