import os


def run():
    from app import app

    host = os.getenv("HOST") or "0.0.0.0"
    port = os.getenv("PORT") or 10_000
    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
