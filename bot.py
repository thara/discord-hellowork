import discord
from discord.ext import commands

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Bot {bot.user} on ready")
    await bot.sync_commands()
    print(f"Bot {bot.user} synced commands")


class HelloWorkView(discord.ui.View):
    @discord.ui.button(label="無職", style=discord.ButtonStyle.primary)
    async def on_clicked_no_job(self, button, interaction):
        await switch_role(interaction, "無職", "無職オンライン")

    @discord.ui.button(label="無職オンライン", style=discord.ButtonStyle.danger)
    async def on_clicked_no_job_online(self, button, interaction):
        await switch_role(interaction, "無職オンライン", "無職")

    @discord.ui.button(label="有職", style=discord.ButtonStyle.success)
    async def on_clicked_employed(self, button, interaction):
        guild = interaction.guild
        member = interaction.user

        role_removed = False
        for role_name in ["無職", "無職オンライン"]:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                if role in member.roles:
                    await member.remove_roles(role)
                    role_removed = True

        if role_removed:
            await interaction.response.send_message(
                f"🎊 {member.name} が 有職 になりました 🎊", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{member.name} は すでに 有職 です 🐝", ephemeral=True
            )


@bot.slash_command(
    name="hello_work",
    description="ハローワーク（公共職業安定所）は、仕事をお探しの方や求人事業主の方に対して、さまざまなサービスを無償で提供する、国（厚生労働省）が運営する総合的雇用サービス機関です。",
)
async def button(ctx):
    await ctx.respond("今まで何してたんだ？", view=HelloWorkView())


async def switch_role(interaction, new_role_name, before_role_name):
    guild = interaction.guild
    member = interaction.user

    new_role = discord.utils.get(guild.roles, name=new_role_name)
    if new_role:
        if new_role in member.roles:
            await interaction.response.send_message(
                f"{member.name} は すでに {new_role.name} です ♨️"
            )
        else:
            await member.add_roles(new_role)
            await interaction.response.send_message(
                f"{member.name} が {new_role.name} になりました ✅"
            )

            before_role = discord.utils.get(guild.roles, name=before_role_name)
            if before_role:
                if before_role in member.roles:
                    await member.remove_roles(before_role)
    else:
        await interaction.response.send_message("Role not found ❌")
