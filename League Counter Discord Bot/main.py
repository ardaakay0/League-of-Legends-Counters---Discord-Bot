import env
import discord
from discord.ext import commands
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.content.startswith("!lc"):
        #Mesaji alir ve komut olan !lc'yi disarida tutar.
        champ = message.content[4:]
        #Birden fazla kelimeye sahip olan sampiyonlarin arasindaki bosluklari "-" ile ayirir. 
        #Bunun sebebi linkte boyle kullanilmasi.
        champ = champ.replace(" ","-")
        champs_lists = get_counters(champ)
        embed = lists_to_embed(champs_lists[0],champs_lists[1])
        await message.channel.send(embed = embed)
        print("Done!")
       
def get_counters(champ):
    opts = Options()
    opts.add_argument('-headless')
    opts.add_argument("--window-size=1920,1200")
    driver = Firefox(options=opts)
    
    try:
        url = ("https://www.counterstats.net/league-of-legends/{}".format(champ))
        driver.get(url)

        good_against = []
        bad_against = []

        for i in range(7):
            try:
                good = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[2]/a[{}]/div/div[2]/span[1]".format(i + 1))
                bad = driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div/div[2]/div[3]/a[{}]/div/div[2]/span[1]".format(i + 1))
                good_against.append(good.text)
                bad_against.append(bad.text)
            except NoSuchElementException:
                # Handle the case where the element is not found
                print(f"Element not found for iteration {i + 1}")
                break

        return [good_against, bad_against]

    except Exception as e:
        # Handle other exceptions, such as connection errors or invalid URLs
        print(f"An error occurred: {e}")
        return [[], []]

    finally:
        # Make sure to close the WebDriver
        driver.quit()

def lists_to_embed(good_against, bad_against):
    embed = discord.Embed(
        title="Matchups",
        description="Showing good and bad matchups",
        color=discord.Color.green()
    )

    # Adding field for 'good_against'
    good_list = "\n".join([f"{i + 1}. {champion}" for i, champion in enumerate(good_against)])
    embed.add_field(name="Good Against", value=good_list, inline=False)

    # Adding field for 'bad_against'
    bad_list = "\n".join([f"{i + 1}. {champion}" for i, champion in enumerate(bad_against)])
    embed.add_field(name="Bad Against", value=bad_list, inline=False)

    return embed

client.run(env.token_id)