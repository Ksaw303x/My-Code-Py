from discord_webhook import DiscordWebhook, DiscordEmbed


if __name__ == '__main__':
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/683788011783323763/vlWC_BRK3K5FhwPDNEB7OLybUQNhr0_n2l2ffoPkryTuUFlZ7NJmt2eRiAgYEYqsGy5E')
    with open("image.jpeg", "rb") as f:
        data = f.read()
        type(data)
        webhook.add_file(file=data, filename='schedule.png')

    # create embed object for webhook
    embed = DiscordEmbed(
        title='Schedule',
        description='Lorem ipsum dolor sit',
        color='03b2f8',
    )
    embed.set_image(url='attachment://example.jpg')

    # add embed object to webhook
    webhook.add_embed(embed)
    response = webhook.execute()
