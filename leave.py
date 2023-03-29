import discord
import json
from discord.ext import commands

# 一個無法按的按鈕


class Null(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

    link = discord.ui.Button(label='多元的資訊服務', style=discord.ButtonStyle.gray, url='https://www.dcadminbot.cf/')
    self.add_item(link)


class Lifted(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="解除合作", custom_id="lifted", row=0, style=discord.ButtonStyle.red)
    async def first_button_callback(self, button, interaction):
        # 開啟資料檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)

            # 檢查是否為合作管理員發出
            role = interaction.guild.get_role(
                data[str(interaction.guild.id)]["set"]["role"])
            if not role in interaction.user.roles:
                embed = discord.Embed(
                    title="權限不足", description=F"只有{role.mention}能使用")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # 移除串列資料
            data[str(interaction.guild.id)]["partners"].remove(
                int(interaction.message.content))
            data[interaction.message.content]["partners"].remove(
                interaction.guild.id)

        # 上傳資料
        with open(path, "w") as file:
            json.dump(data, file)

        # 編輯原訊息
        guild = interaction.message.embeds[0].title
        embed = discord.Embed(
            title="解除合作",
            description=F"""因**`{guild}`**將機器人退出
            所以由{interaction.user.mention}確認解除合作關係""")
        await interaction.message.edit(embed=embed, view=Null())
        await interaction.response.defer()

    @discord.ui.button(label="保留合作", custom_id="keep", row=1, style=discord.ButtonStyle.gray)
    async def second_button_callback(self, button, interaction):
        # 開啟資料檔案
        with open("database/guild.json", "r") as file:
            data = json.load(file)

        # 檢查是否為合作管理員發出
        role = interaction.guild.get_role(
            data[str(interaction.guild.id)]["set"]["role"])
        if not role in interaction.user.roles:
            embed = discord.Embed(
                title="權限不足",
                description=F"只有{role.mention}能使用")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # 編輯原訊息
        guild = interaction.message.embeds[0].title
        embed = discord.Embed(
            title=guild,
            description=F"""雖機器人已離開{guild}
            但由{interaction.user.mention}確認保留合作關係""")
        await interaction.message.edit(embed=embed, view=Null())
        await interaction.response.defer()


class leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(Lifted())

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # 開啟資料檔案
        path = "database/guild.json"
        with open(path, "r") as file:
            data = json.load(file)
        if not str(guild.id) in data.keys():
            return

        # 搜尋所有合作群組
        for partner in data[str(guild.id)]["partners"]:
            try:
                partner = await self.bot.fetch_guild(partner)
                channel = await partner.fetch_channel(data[str(partner.id)]["set"]["channel"])
                embed = discord.Embed(
                    title=guild,
                    description=F"""檢測到機器人已離開
                    合作群**`{guild}`**
                    請問是否要解除合作關係?""")
                await channel.send(content=guild.id, embed=embed, view=Lifted())
            except:
                continue


def setup(bot):
    bot.add_cog(leave(bot))
