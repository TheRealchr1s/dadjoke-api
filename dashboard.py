from quart import Quart, jsonify, request, redirect
import json
import random
import aiohttp
import aiofiles

# --- init stuff ---
app = Quart(__name__)
session = aiohttp.ClientSession()
client_id = "511267168352993295"
client_secret = "ZKHEylOo_V6ecDmo98Vr9padPYsC-LTh"
redirect_uri = "http://web-dashboard.cf"
redir = r"https://discordapp.com/api/oauth2/authorize?client_id=511267168352993295&redirect_uri=http%3A%2F%2Fweb-dashboard.cf%2Fauthorize&response_type=token&scope=identify"
bearer_url = "https://discordapp.com/oauth2/token?client_id={}&client_secret={}&grant_type=authorization_code&code={}&redirect_uri={}&scope=identify"
# https://discordapp.com/oauth2/token?client_id=511267168352993295&client_secret=ZKHEylOo_V6ecDmo98Vr9padPYsC-LTh&grant_type=authorization_code&code=aKlaHpi6wC4HrmFR7nYY5OysGiAHRm&redirect_uri=http://web-dashboard.cf&scope=identify
allowed = ["246938839720001536", "455289384187592704", "300088143422685185", "356091260429402122"]
# --- ---

@app.route("/")
@app.route("/info")
async def info():
    return redirect(redir)

@app.route("/authorize")
@app.route("/authorise")
async def authorize():
    if request.args.get("error"):
        return """
            <style>
            background: linear-gradient(110deg, #fdcd3b 60%, #ffed4b 60%);
            </style><h1>Unauthorized</h1>
            """
    d = f"""
    <html>
    <head>
    <style>
    background: linear-gradient(110deg, #fdcd3b 60%, #ffed4b 60%);
    </style>
    <h1 style="font-family: 'Verdana'"><a href="https://www.google.com" id="test">Click here to go to the dashboard test.</a></h1>
    <script>
    var doc = document.getElementById("test");
    if (window.location.hash) {{
        doc.href = "{request.url.replace("/authorize", "")}/check?" + window.location.hash.substring(1).split("&")[0];
    }}
    </script>
    </head>
    </html>
    """
    return d

@app.route("/check")
async def check():
    tk = request.args.get("access_token")
    if not tk:
        return "<h1>Unauthorized</h1>"
    header = {"Authorization": f"Bearer {tk}"}
    async with session.get("https://discordapp.com/api/users/@me", headers=header) as r:
        resp = await r.json()
        if resp['id'] not in allowed:
            return "<h1>Unauthorized</h1>"
        return redirect(request.url.replace("/check", f"/dashboard"))

@app.route("/dashboard")
async def dashboard():
    tk = request.args.get("access_token")
    if not tk:
        return "<h1>Unauthorized</h1>"
    header = {"Authorization": f"Bearer {tk}"}
    async with session.get("https://discordapp.com/api/users/@me", headers=header) as r:
        resp = await r.json()
        if resp['id'] not in allowed:
            return "<h1>Unauthorized</h1>"
        returned = request.args.get("msg")
        if returned == "return_cb":
            return f"""
        <title>chr1sBoard</title>
        <script>alert('INFO: Restarting Cleverbot')</script>
        <h1 style="font-family: 'Verdana'">Welcome, {resp['username']}!<br><br></h1>
        <p style="font-family: 'Verdana'">Logged in as {resp['username']}#{resp['discriminator']} ({resp['id']})<br><br><br></p>
        <h1 style="font-family: 'Verdana'">chr1sBot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/chr1sbot?access_token={tk}';">Restart</button>
        <h1 style="font-family: 'Verdana'">Cleverbot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/cleverbot?access_token={tk}';">Restart</button>
        """
        if returned == "return_c1":
            return f"""
        <title>chr1sBoard</title>
        <script>alert('INFO: Restarting chr1sBot')</script>
        <h1 style="font-family: 'Verdana'">Welcome, {resp['username']}!<br><br></h1>
        <p style="font-family: 'Verdana'">Logged in as {resp['username']}#{resp['discriminator']} ({resp['id']})<br><br><br></p>
        <h1 style="font-family: 'Verdana'">chr1sBot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/chr1sbot?access_token={tk}';">Restart</button>
        <h1 style="font-family: 'Verdana'">Cleverbot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/cleverbot?access_token={tk}';">Restart</button>
        """
        return f"""
        <title>chr1sBoard</title>
        <h1 style="font-family: 'Verdana'">Welcome, {resp['username']}!<br><br></h1>
        <p style="font-family: 'Verdana'">Logged in as {resp['username']}#{resp['discriminator']} ({resp['id']})<br><br><br></p>
        <h1 style="font-family: 'Verdana'">chr1sBot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/chr1sbot?access_token={tk}';">Restart</button>
        <h1 style="font-family: 'Verdana'">Cleverbot</h1>
        <button type="button" onclick="window.location = 'http://web-dashboard.cf/restart/cleverbot?access_token={tk}';">Restart</button>
        """

@app.route("/restart/cleverbot")
async def restart_cb():
    tk = request.args.get("access_token")
    if not tk:
        return "<h1>Unauthorized</h1>"
    header = {"Authorization": f"Bearer {tk}"}
    async with session.get("https://discordapp.com/api/users/@me", headers=header) as r:
        resp = await r.json()
        if resp['id'] not in allowed:
            return "<h1>Unauthorized</h1>"
    async with aiofiles.open("/home/cleverbot/restart.txt", "w") as f:
        await f.write("1")
    return redirect(f"http://web-dashboard.cf/dashboard?msg=return_cb&access_token={tk}")

@app.route("/restart/chr1sbot")
async def restart_c1():
    tk = request.args.get("access_token")
    if not tk:
        return "<h1>Unauthorized</h1>"
    header = {"Authorization": f"Bearer {tk}"}
    async with session.get("https://discordapp.com/api/users/@me", headers=header) as r:
        resp = await r.json()
        if resp['id'] not in allowed:
            return "<h1>Unauthorized</h1>"
    async with aiofiles.open("/home/bot/restart.txt", "w") as f:
        await f.write("1")
    return redirect(f"http://web-dashboard.cf/dashboard?msg=return_c1&access_token={tk}")

app.run(host='0.0.0.0', debug=True, port=80)