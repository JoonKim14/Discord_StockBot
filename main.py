import yfinance as yf

from matplotlib import pyplot as plt

from datetime import datetime,timedelta,date

import discord

client = discord.Client()

# TickerSymbol is a String that represents a certain company

# Date is written like 2020-01-01, 2005-05-14, etc...

# Plot is an image that shows the stock change throughout certain period

#Let's the user know that the discord bot is Online.
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # If the message is sent by the bot, it ignores it.
    if message.author == client.user:
        return

    # If the message starts with $plot,
    # It consumes TickerSymbol and produces a plotted image
    # TickerSymbol -> Plot
    if message.content.startswith('$plot'):

        #get the TickerSymbol after the $plot,
        riptext = message.content.split(" ", 1)[1:]

        tickerData = yf.Ticker(riptext[0])

        #set the beginning time to a year ago
        begin = datetime.now() - timedelta(days=365)

        #if the history does not exist,
        if tickerData.history(period='1d', start=begin, end=date.today()).empty:
            # print that it's an invalid input
            await message.channel.send("Invalid Input")

            return

        #if the history does exist,
        else:
            tickerDf = tickerData.history(period='1d', start=begin, end=date.today())

            # plot the TickerSymbol
            plt.plot(tickerDf.Open)

            # save the plotted image
            plt.savefig('plot.png', dpi=300, bbox_inches='tight')

            # send the plotted image on the channel
            await message.channel.send(file=discord.File('plot.png'))

            # clear the plot
            plt.clf()

            return

        return

    # If the message starts with $between,
    # It consumes Date, Date ,and TickerSymbol and produces a plotted image
    # Date Date TickerSymbol -> Plot
    #   It requires that the first date is older than the second date.
    if message.content.startswith('$between'):

        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[3])

        #Makes the first Date the beginning date
        begin = split_text[1]

        # Makes the second Date the finishing date
        finish = split_text[2]


        if tickerData.history(period='1d', start=begin, end=finish).empty:

            await message.channel.send("Invalid Input")

            return

        else:
            tickerDf = tickerData.history(period='1d', start=begin, end=finish)

            plt.ticklabel_format(style='plain')

            plt.plot(tickerDf.Open)

            # It rotates the x-axis titles by 45 degrees to avoid texts from overlapping
            plt.xticks(rotation=45)

            plt.savefig('plot.png', dpi=300, bbox_inches='tight')

            await message.channel.send(file=discord.File('plot.png'))

            plt.clf()

            return

        return

    # If the message starts with $major_holders,
    # It consumes TickerSymbol and produces the major holders
    if message.content.startswith('$major_holders'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.major_holders)

    # If the message starts with $institutional_holders,
    # It consumes TickerSymbol and produces the institutional holders
    if message.content.startswith('$institutional_holders'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.institutional_holders)

    # If the message starts with $sustainability,
    # It consumes TickerSymbol and produces the sustainability
    if message.content.startswith('$sustainability'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.sustainability)

    # If the message starts with $calendar,
    # It consumes TickerSymbol and produces the events
    if message.content.startswith('$calendar'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.calendar)

    # If the message starts with $ISIN,
    # It consumes TickerSymbol and produces the ISIN
    if message.content.startswith('$ISIN'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.isin)

    # If the message starts with $options,
    # It consumes TickerSymbol and produces the options
    if message.content.startswith('$options'):
        split_text = message.content.split()

        tickerData = yf.Ticker(split_text[1])

        await message.channel.send(tickerData.options)

client.run('Put your bot token here!')
