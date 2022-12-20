# Replit - ping this repo using UptimeRobot every 1 hour.

scripts = [
    "dmoj_problem_notifier",
    "shadertoy_notifier",
]
for script in scripts:
    try:
        __import__(script)
    except BaseException as e:
        print(e)

if __name__ == "__main__":
    # make replit ping-able

    app = __import__("flask").Flask('')

    @app.route('/')
    def home():
        return """<center><h1>Hello, World!</h1></center><hr><center>uptime-scripts/0.0.0.0</center>"""

    def run():
        app.run(host='0.0.0.0', port=8080)

    __import__("threading").Thread(target=run, daemon=True).start()

    __import__("time").sleep(120)
    __import__("sys").exit(0)
