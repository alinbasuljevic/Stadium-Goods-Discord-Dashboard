import discord, requests, discord_webhook, datetime, time
from bs4 import BeautifulSoup as bs


TOKEN = 'NTAyMTM4MzMwOTgxMzM1MDQy.XP6ddg.46GgbuIgGQDorbBrdkPeU_5tRwE'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!info'):
        username = message.content.split()[1]
        print (username)
        password = message.content.split()[2]
        print (password)
        msg = 'Fetching Dashboard Info...'
        await message.channel.send(msg)
        s = requests.Session()
        dashboard_url  = s.get('https://sellers.stadiumgoods.com/users/sign_in')
        soup = bs(dashboard_url.text, 'lxml')
        auth_token = soup.find('meta', attrs={'name':'csrf-token'}).get('content')
        payload = {
            'utf8':'✓',
            'authenticity_token':auth_token,
            'user[email]':username,
            'user[password]':password,
            'user[remember_me]':'0',
            'commit':'Login'
            }
        headers = {
            'origin': 'https://sellers.stadiumgoods.com',
            'referer': 'https://sellers.stadiumgoods.com/users/sign_in',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
            }
        
        login_request = s.post('https://sellers.stadiumgoods.com/users/sign_in', data=payload, headers=headers, allow_redirects=True)
        if login_request.url == 'https://sellers.stadiumgoods.com/sellers/dashboard':
            print ('LOGGED IN!')
            webhook = '###########'
            soup = bs(login_request.text, 'lxml')
            list_of_text = []
            header_list = []
            for data in soup.find_all('h2'):
                list_of_text.append(data.text)
            shoes_listed = soup.find('h2', attrs={'class':'shoes-listed'})
            paid_amount = soup.find('h2', attrs={'class':'paid-amount'})
            to_be_paid = soup.find('h2', attrs={'class':'to-be-paid'})
            shoes_sold_last = soup.find('h2', attrs={'class':'shoes-sold-last-7'})
            embed = discord.Embed(title='{} Stadium Goods Sellers Portal'.format(soup.find('h1').text), description='Last Updated on {}'.format(datetime.date.today()), inline=True)
            embed.add_field(name='Account Number', value=list_of_text[1], inline=True)
            embed.add_field(name='Current Shoes in Inventory', value=shoes_listed.text, inline=False)
            embed.add_field(name='Total Sales', value=paid_amount.text, inline=False)
            embed.add_field(name='Amount to be Paid', value=to_be_paid.text, inline=False)
            embed.add_field(name='Number of Shoes Sold in the Past 7 Days', value=shoes_sold_last.text, inline=False)
 
        else:
            print ('ERROR!')

        await message.channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
