from flask import Flask, request, jsonify, render_template
import discord
import asyncio
import threading

app = Flask(__name__)

# Initialize Discord client outside the request handling
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@app.route('/')
def index():
    return render_template('index.html')

def start_discord_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    @client.event
    async def on_ready():
        print('Discord client is ready.')

    client.run('')  # Replace with client token

# Run Discord client in a background thread
threading.Thread(target=start_discord_bot, daemon=True).start()

@app.route('/upload', methods=['POST'])
def upload_files():
    # Get multiple files from the request
    files = request.files.getlist('file')

    if not client.is_closed():
        # Create a list to store futures for each file upload
        futures = []
        for file in files:
            future = asyncio.run_coroutine_threadsafe(send_file_to_discord(file), client.loop)
            futures.append(future)

        # Wait for all futures to complete and collect results
        results = [future.result() for future in futures]

    return jsonify({'message': f'{len(files)} files uploaded successfully!'})

async def send_file_to_discord(file):
    print("Sending file to Discord:", file.filename)
    channel = client.get_channel()  # Replace with channel ID
    message = await channel.send(file=discord.File(file.stream, filename=file.filename))
    print(f"File sent to Discord: {file.filename}")
    return message

if __name__ == '__main__':
    app.run(debug=True)
