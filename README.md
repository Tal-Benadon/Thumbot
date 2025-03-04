# ThumbBot

ThumbBot is a Discord bot that automatically downloads and shares videos from various social media platforms when links are posted in channels.

## Features

- Monitors Discord channels for links to supported video platforms
- Automatically downloads videos and posts them directly in the channel
- Supports multiple video providers including:
  - Reddit
  - Instagram Reels
  - Facebook videos and reels
- Handles size limitations and format conversions

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Discord server with appropriate permissions

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Tal-Benadon/Thumbot.git
   cd thumbbot
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

### Running the Bot

Run the bot using:
```
python main.py
```

### Docker Support

You can also run the bot using Docker:

```
docker build -t thumbbot .
docker run -d -e DISCORD_TOKEN=your_discord_bot_token_here thumbbot
```

#### Using Custom Providers

You can mount your own custom providers.json file to override the default providers:

```
docker run -d \
  -e DISCORD_TOKEN=your_discord_bot_token_here \
  -v /path/to/your/providers.json:/app/providers.json \
  thumbbot
```

**Important Notes About Providers:**
- Currently, custom providers.json can only be used to *remove* providers from the default list
- Adding new providers requires additional custom code in the downloader component
- Twitter/X integration is currently in development

Example of a custom providers.json file:
```json
{
  "providers": [
    "reddit",
    "instagram.com/reel"
    // Facebook providers removed from this example
  ]
}
```

## How It Works

1. The bot monitors all messages in channels it has access to
2. When a URL from a supported provider is detected, it attempts to download the video
3. The video is processed and then posted directly in the channel
4. The temporary video file is automatically deleted after posting

## Project Structure

- `bot/`: Contains the Discord bot implementation
- `downloader/`: Contains the video downloading and processing logic
- `providers.json`: Configuration file for supported video platforms

## Microservices Version

For larger deployments, check out the microservices version where the bot and downloader components are separated into independent repositories:

- **Bot Service**: Written in Node.js, handles Discord interactions and communication
  - [ThumbBot Discord Service Repository](https://github.com/Tal-Benadon/thumbot_bot)
- **Downloader Service**: Written in Python, handles video downloading and processing
  - [ThumbBot Downloader Service Repository](https://github.com/Tal-Benadon/thumbot_downloader)

The microservices architecture provides several advantages:
- Independent scaling of each component
- Ability to update components separately
- Improved resilience and fault isolation

Functionally, the microservices version operates similarly to this monolithic version but is better suited for environments that want to scale their services independently.

## Configuration

You can remove supported video providers by editing the `providers.json` file.

## Troubleshooting

- Ensure your bot has the "Message Content Intent" enabled in the Discord Developer Portal
- Some providers have rate limits that might affect downloading capacity
- Maximum file size for Discord uploads is 8MB for non-boosted servers

## License

See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
