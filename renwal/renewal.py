#-*- coding: utf-8 -*-
from discord.ext import tasks
import enum
import discord
import os
import datetime
import random
import sqlite3
import asyncio
from discord import Colour, Interaction, ui,app_commands,Button,ButtonStyle,SelectMenu,SelectOption
from discord.ext import commands
from renewal_class import *
from skill import Skill, skillModify
KST=datetime.timezone(datetime.timedelta(hours=9))
class MyClient(discord.Client):
  @tasks.loop(time=datetime.time(hour=8,minute=0,second=0,tzinfo=KST))
  async def daily_message(self):
    channel=self.get_channel(955246009427038261)
    await channel.send("ddd")
  async def on_ready(self):
    await self.wait_until_ready()
    await tree.sync(guild= discord.Object(id=955246008923742209))
    print(f"{self.user} 에 로그인하였습니다!")
    self.daily_message.start()
    await self.bt(["코드 최적화","그림쟁이 구","개발 연기"])
  async def on_member_join(self,member:discord.Member):
    try:
      guild=member.guild
      role=discord.utils.get(guild.roles,name="ㅇㅇㅇㅇ")
      await member.add_roles(role)
      #await member.send(f"{member.name}님 안녕하세요! ")
    except:
      pass
  async def bt(self,items):
    while not client.is_closed():
        for g in items:
            await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
            await asyncio.sleep(5)
  
class reportModal(ui.Modal, title="건의"):
  answer=ui.TextInput(
        custom_id="생성",
        label="건의하기",
        style=discord.TextStyle.long,
        placeholder="건의사항을 적어주세요.",
        required=True,
        max_length=500,
      )  
  async def on_submit(self, interaction: discord.Interaction):
    con=sqlite3.connect(r'./rpg.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS report(value TEXT,user TEXT)")
    cur.execute("INSERT INTO report VALUES(?,?)",(self.answer.value,interaction.user.id,))
    con.commit()
    await interaction.response.send_message("건의사항이 접수되었습니다.",ephemeral=True)
class ReinforceItem(enum.Enum):
  무기=0
  투구=1 
  티셔츠=2
  벨트=3
  장갑=4
  보조무기=5
  갑옷=6
  하의=7
  신발=8
  반지1=9
  반지2=10
  목걸이=11
  팔찌=12

class Status(enum.Enum):
  힘 = 'str'
  민첩 = 'dex'
  지능 = 'int'
  행운 = 'luck'
  체력 = 'hp'
  마나 = "mp"

class Inventory(enum.Enum):
  무기 = "_weapon"
  방어구 = "_wear"
  소비 = "_use"
  기타 = "_etc"
  캐시 = "_cash"

intents= discord.Intents.all()
client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
con = sqlite3.connect(r"./rpg.db",isolation_level=None)
cur = con.cursor()
class Color(enum.Enum):
  레드=discord.Color.red()
  블루=discord.Color.blue()
  노랑=discord.Color.yellow()
  초록=discord.Color.green()
  골드=0xffd700
  

#./rpg.db
#/생성 <닉네임>
@tree.command(guild= discord.Object(id=955246008923742209),name="생성", description="아이디를 생성합니다.")
async def register(interaction: discord.Interaction, 닉네임: str):
  embed = discord.Embed(title="아이디 생성")
  value=""
  if len(닉네임) > 10 and len(닉네임)<=2:
    value="아이디 길이는 2~10자 사이로 정해주세요."
  cur.execute("SELECT * FROM user_stat WHERE id = ?",(interaction.user.id,))
  if cur.fetchone():
    value="이미 계정이 있습니다."
  cur.execute("SELECT * FROM user_stat WHERE name = ?",(닉네임,))
  if cur.fetchone():
    value="이미 있는 닉네임 입니다."
  
  if value:
    embed.add_field(name="아이디 생성 실패",value=value)
    return await interaction.response.send_message(embed=embed,ephemeral=True)
  embed= discord.Embed(title="아이디 생성")
  embed.add_field(name="닉네임",value=닉네임)
  cur.execute("INSERT INTO user_data VALUES(?, ?, ?, ?, ? , ?, ?)", (닉네임,interaction.user.id, 1, 0, 500,0,str(interaction.user.display_avatar.url),))            
  cur.execute("INSERT INTO user_stat VALUES(?, ?, ?, ?, ? ,? ,?, ?, ?, ?)",(닉네임,interaction.user.id,1,1,1,1,1,0,3,1))
  inventory=Default(interaction.user.id)
  inventory.isInventory()
  inventory.isItem()
  inventory.first()
  await interaction.response.send_message(embed=embed,ephemeral=True)

@tree.command(guild= discord.Object(id=955246008923742209),name="팀", description="역할")
async def role(interaction:Interaction,색:Color):
  guild=interaction.user.guild 
  other=[]
  for i in Color:
    role=discord.utils.get(guild.roles,name=i.name)
    if not role:
      role= await guild.create_role(name=i.name,hoist=True,color=i.value)
    if not i.name==색.name:
      other.append(role)
    else:
      mine=role
      print(mine)
  category=discord.utils.get(guild.categories,name="팀 채팅방")
  if not category:
    category = await guild.create_category(name="팀 채팅방")   
  channel=discord.utils.get(guild.channels,name=f"{색.name}팀-채팅방")
  if not channel:
    overwrites= {
      guild.default_role:discord.PermissionOverwrite(view_channel=False),
      mine:discord.PermissionOverwrite(send_messages=True,view_channel=True),
    }
    await guild.create_text_channel(name=f"{색.name}팀-채팅방",category=category,overwrites=overwrites)
  for i in other:
    await interaction.user.remove_roles(i)
  await interaction.user.add_roles(mine)
  await interaction.response.send_message(f"{색.name}팀으로 바뀌었습니다.",ephemeral=True)
  #if not role in guild.roles:
  #  guild.create_role(name="이름",hoist=True,colour=discord.Colour(3),)
@tree.command(guild= discord.Object(id=955246008923742209),name="공포의쓴맛", description="공포의쓴맛을줄수있다.")
async def ss(interaction:discord.Interaction,유저:discord.Member,시간:int=30,이유:str="그냥"):
  if interaction.user.guild_permissions.administrator:
    await 유저.timeout(datetime.timedelta(seconds=시간),reason=이유)
    #datetime.datetime.now()+datetime.timedelta(seconds=시간)
    await interaction.response.send_message(f"{유저} {시간}초 조용해짐! 사유:{이유}",ephemeral=True)
  else:
    await interaction.response.send_message("쓴맛을 줄 권한이 없어요!",ephemeral=True)
@tree.command(guild= discord.Object(id=955246008923742209),name="밴", description="밴밴")
async def dd(interaction:discord.Interaction,유저:discord.Member,시간:int=1,이유:str="그냥"):
  if interaction.user.guild_permissions.administrator:
    await 유저.ban(delete_message_days=시간,reason=이유)
    await interaction.response.send_message(f"{유저} 밴됨! 이유:{이유}",ephemeral=True)
  else:
    await interaction.response.send_message("밴할 권한이 없어요!",ephemeral=True)
@tree.command(guild= discord.Object(id=955246008923742209),name="킥", description="킥킥")
async def dd(interaction:discord.Interaction,유저:discord.Member,이유:str="그냥"):
  if interaction.user.guild_permissions.administrator:
    await 유저.kick(reason=이유)
    await interaction.response.send_message(f"{유저} 킥됨! 사유:{이유}",ephemeral=True)
  else:
    await interaction.response.send_message("킥할 권한이 없어요!",ephemeral=True)

#/정보 <유저>  
@tree.command(guild= discord.Object(id=955246008923742209),name="정보", description="캐릭터 정보를 확인합니다.")
async def info(interaction:discord.Interaction, 유저 : discord.Member):
  cur.execute("SELECT * FROM user_data WHERE id = ?",(유저.id,))
  check=cur.fetchone()
  if not check:
    embed= discord.Embed(title="에러")
    embed.add_field(name="존재하지 않는 프로필입니다.",value='\u200b')
    return await interaction.response.send_message(embed=embed,ephemeral=True)
  async def button_callback(interaction:discord.Interaction):
    embed=discord.Embed(title="스테이터스")
    embed.set_thumbnail(url=유저.avatar)
    cur.execute("SELECT name,str,dex,int,luck,hp,mp,stat_point,skill_point FROM user_stat WHERE id =?",(유저.id,))
    check=cur.fetchone()
    stat=['닉네임','힘','민첩','지능','행운','체력',"마나",'남은 스테이터스 포인트','남은 스킬 포인트']
    true=[False,True,True,True,True,True,True,False,False]
    for i in range(9):
      embed.add_field(name=stat[i],value=check[i],inline=true[i])
    button = ui.Button(label="정보로 이동",style=ButtonStyle.green)
    view=ui.View(timeout=0)
    view.add_item(button)
    button.callback=info_callback
    await interaction.response.edit_message(embed=embed,view=view)
  async def info_callback(interaction:discord.Interaction):
    embed=discord.Embed(title="정보",color=유저.color)
    embed.set_thumbnail(url=유저.avatar)
    cur.execute("SELECT name,level,exp,money,class,url FROM user_data WHERE id = ?",(유저.id,))
    check = cur.fetchone()
    display=["닉네임","레벨","","돈","",""]
    for i in range(len(check)):
      if i==2:
        guild= client.get_guild(955246008923742209)
        print(int(check[i-1]/15))
        exp = Exp(check[i],check[i-1]*30*int(check[i-1]/15+1))
        block_id=["0_","1_","2_","3_","4_","5_","6_","7_","8_","9_","10","9_5"]
        block_list=[discord.utils.get(guild.emojis,name=i) for i in block_id]
        embed.add_field(name=f"경험치 {exp.string()} ({round(exp.percent(),1)}%)",value=exp.block(block_list),inline=False)
      elif i==4:
        transfer=Class(check[i])
        embed.add_field(name="직업",value=transfer.display(),inline=True)
      elif i ==5:
        pass
      else:
        embed.add_field(name=display[i],value=check[i],inline=True)
    view=ui.View(timeout=0)
    button = ui.Button(label="스테이터스로 이동",style=ButtonStyle.green)
    button.callback=button_callback
    view.add_item(button)
    await interaction.response.edit_message(embed=embed,view=view)  
  button = ui.Button(label="정보로 이동",style=ButtonStyle.green)
  view=ui.View(timeout=0)
  view.add_item(button)        
  button.callback=info_callback
  await interaction.response.send_message("",view=view,ephemeral=True)

@tree.command(guild= discord.Object(id=955246008923742209),name="던전초기화", description="던전 상태를 초기화합니다.")
async def dungeonreset(interaction:Interaction):
  a=random.randint(10000,99999)
  class dungeonModal(ui.Modal, title=f"초기화 코드 : {a}"):
    answer=ui.TextInput(
          label=f"초기화 코드 : {a}",
          style=discord.TextStyle.short,
          placeholder="코드를 적어주세요.",
          required=True,
          max_length=5,
        )    
    async def on_submit(self, interaction: Interaction):
      if int(self.answer.value)==a:
        dungeon_dic[interaction.user.id]=False
        await interaction.response.send_message("초기화 성공",ephemeral=True)
      else:
        await interaction.response.send_message("초기화 실패",ephemeral=True)
  await interaction.response.send_modal(dungeonModal())
#/스텟 <스텟> <포인트>
@tree.command(guild= discord.Object(id=955246008923742209),name="스텟", description="스테이터스를 올립니다.")
async def status(interaction:discord.Interaction, 스텟:Status, 포인트:int ):
  cur.execute("SELECT stat_point,hp FROM user_stat WHERE id = ?",(interaction.user.id,))
  check=cur.fetchone()
  if 포인트 > check[0]:
    title="스테이터스 에러"
    name="스테이터스 포인트가 모자랍니다."
  elif 포인트 < 0:
    title="스테이터스 에러"
    name="스테이터스가 0보다 작을수는 없습니다."
  elif 포인트+check[1]>20 and 스텟.name=="체력":
    title="스테이터스 에러"
    name="체력 스텟은 20보다 클수 없습니다."
  else: 
    title="스테이터스"
    name=f"**{스텟.name}**을 **+{포인트}** 만큼 올렸습니다." 
    cur.execute(f"UPDATE user_stat SET {스텟.value} = {스텟.value}+{포인트},  stat_point=stat_point-{포인트}  WHERE id = ?",(interaction.user.id,))    
  embed=discord.Embed(title=title)
  embed.add_field(name=name,value='\u200b')
  await interaction.response.send_message(embed=embed,ephemeral=True)

#/강화소 <장비>
@tree.command(guild= discord.Object(id=955246008923742209),name="강화소", description="착용중인 아이템을 강화합니다.")
async def reinforcement(interaction: discord.Interaction, 장비:ReinforceItem):
  con=sqlite3.connect(r"./item.db",isolation_level=None)
  cur=con.cursor()
  if 장비.value != 0:
    cur.execute(f"SELECT * FROM '''{interaction.user.id}_wear''' WHERE part = ? AND wear = ? ",(장비.value,1,))
  else:
    cur.execute(f"SELECT * FROM '''{interaction.user.id}_weapon''' WHERE wear = ?",(1,))
  check =cur.fetchone()
  if not check:
    embed=discord.Embed(title="강화 에러")
    embed.add_field(name="아이템을 착용하고 있지 않습니다.",value="\u200b")
    await interaction.response.send_message(embed=embed)
  else:
    embed=discord.Embed(title="아이템 강화")
    itemInfo=['이름','강화','등급','레벨제한','힘','민첩','지능','행운','체력','마나']
    true =[True,True,True,False,True,True,True,True]
    for i in range(0,7):
      embed.add_field(name=itemInfo[i],value=check[i],inline=true[i])
    embed.add_field(name="마나",value=check[8])
    if 장비.value == 0:
      embed.add_field(name="데미지",value=check[9])
      embed.set_thumbnail(url=check[14])
    else:
      embed.add_field(name="체력",value=check[7])
      embed.set_thumbnail(url=check[16])
    view = ui.View()
    cur.execute(f"SELECT item_amount FROM '''{interaction.user.id}_etc''' WHERE item_code = ?",(1,))
    amount = cur.fetchone()
    if amount==None:
      amount=0
    else:
      amount=amount[0]
    con = sqlite3.connect(r"./rpg.db",isolation_level=None)
    cur = con.cursor()
    cur.execute("SELECT money FROM user_data WHERE id = ?",(interaction.user.id,))
    gold= cur.fetchone()[0]
    if check[2]=="F": 
      return await interaction.response.send_message("강화가 불가능한 아이템입니다.",ephemeral=True)
    rein = Reinforce(gold,amount,check[1],check[2])
    a,b=rein.display()
    if not a or not b:
      await interaction.response.send_message("강화가 불가능한 아이템입니다.",ephemeral=True)
    embed.add_field(name="강화 확률",value=f"{b}%",inline=False)
    embed.add_field(name="재료",value=f"{a}골드 , 강화의 서 {int(a/50)}개",inline=False)
    select = ui.Select(placeholder=("원하는 스텟을 골라주세요." if not rein.require() else "골드 또는 재료가 부족합니다."),disabled=rein.require(),options=[
      SelectOption(label="힘",value='str',description="전사 직업군의 주스텟"), 
      SelectOption(label="민첩",value='dex',description="궁수 직업군의 주스텟"),
      SelectOption(label="지능",value='int',description="마법사 직업군의 주스텟"),
      SelectOption(label="행운",value='luck',description="도적 직업군의 주스텟"),
      ])
    if 장비.value !=0:
      select.options.append(SelectOption(label="체력",value="hp",description="캐릭터의 추가 체력"))
    select.options.append(SelectOption(label="마나",value="mp",description="캐릭터의 추가 마나"))
    view.add_item(select)
    async def select_callback(interaction:discord.Interaction):
      con=sqlite3.connect(r"./rpg.db",isolation_level=None)
      cur=con.cursor()
      cur.execute(f"UPDATE user_data SET money = money -{a} WHERE id = ?",(interaction.user.id,))
      con=sqlite3.connect(r"./item.db",isolation_level=None)
      cur=con.cursor()
      cur.execute(f"UPDATE '''{interaction.user.id}_etc''' SET item_amount=item_amount - {int(a/50)} WHERE item_code=1")
      if rein.rein():
        r=random.randint(1,2)
        title="강화성공"
        if select.values[0]=="hp":
          r*=2
        mode=Modify(select.values[0])
        name=f"{mode.statModify()}이 +{r} 올랐다."
        if 장비.value==0:
          cur.execute(f"UPDATE '''{interaction.user.id}_weapon''' SET upgrade = upgrade+1, {select.values[0]}={select.values[0]}+{r} WHERE wear = 1")
        else:
          cur.execute(f"UPDATE '''{interaction.user.id}_wear''' SET upgrade = upgrade+1, {select.values[0]}={select.values[0]}+{r} WHERE wear = 1 AND part= ?",(장비.value,))
      else:
        title="강화실패"
        name="아쉽지만 다음기회에"
      embed=discord.Embed(title=title)
      embed.add_field(name=name,value='\u200b')
      return await interaction.response.edit_message(embed=embed,view=None)
    select.callback =select_callback
    await interaction.response.send_message(embed=embed,ephemeral=True,view=view)

#/던전 <층>
dungeon_dic={}
@tree.command(guild= discord.Object(id=955246008923742209),name="던전", description="던전입니다.")
async def dungeon(interaction:discord.Interaction,층:int):
  skill=Skill(interaction.user.id)
  default = Default(interaction.user.id)
  global dungeon_dic
  DunGeon=Dungeon(interaction.user.id,dungeon_dic,층)
  default.isInventory()
  default.isItem()
  skill.isSkill()
  effect={}
  dungeon_dic,content=DunGeon.go()
  if content:
    return await interaction.response.send_message(content=content,ephemeral=True)
  global hp,mp,damage,enemy
  dungeon_dic,hp,mp,damage,enemy=DunGeon.stat()
  def em():

    effect_list=""
    for key,value in effect.items():
      name,value=skill.fight(key,value)
      effect_list += f"{name}{value}"
    embed=discord.Embed(title=f"{enemy[0]} {effect_list}")
    embed.set_thumbnail(url=enemy[6])
    embed.add_field(name=f"{enemy[1]}❤",value="\u200b",inline=True)
    embed.add_field(name=f"{enemy[2]}⚔",value="\u200b",inline=True)
    embed.add_field(name="나",value="\u200b",inline=False)
    embed.add_field(name=f"{hp}❤",value="\u200b",inline=True)
    embed.add_field(name=f"{mp}🔋",value="\u200b",inline=True)
    embed.add_field(name=f"{damage.display()}⚔",value="\u200b",inline=True)
    return embed 
  def vi():
    view=ui.View()
    attack=ui.Button(style=discord.ButtonStyle.green,emoji="⚔",label="공격하기")
    use=ui.Button(style=discord.ButtonStyle.gray,emoji="💊",label="아이템",)
    guard=ui.Button(style=discord.ButtonStyle.gray,emoji="🔮",label="스킬사용",disabled=skill.canskill())
    run=ui.Button(style=discord.ButtonStyle.red,emoji="👟",label="도망가기",disabled=True)
    view.add_item(attack)
    view.add_item(use)
    view.add_item(guard)
    view.add_item(run)
    attack.callback = attack_callback
    guard.callback = skill_select_callback
    use.callback= item_select_callback
    return view
  
  async def item_select_callback(interaction:discord.Interaction):
    embed= em()
    con= sqlite3.connect(r"./item.db")
    cur=con.cursor()
    cur.execute(f"SELECT item_code,item_name,item_amount,trade FROM '''{interaction.user.id}_use''' WHERE item_code BETWEEN 1 AND 50 AND item_amount IS NOT 0")
    getItem=cur.fetchall()
    view = ui.View()
    select = ui.Select(placeholder="아이템 사용",options=[SelectOption(label="돌아가기",value=-1)])
    for i in range(len(getItem)):
      select.options.append(SelectOption(label=f"{getItem[i][1]} {getItem[i][2]}개",value=getItem[i][0],description=("회복 아이템")))
    view.add_item(select)
    async def item_effect_callback(interaction:discord.Integration):
      if int(select.values[0]) == -1:
        await interaction.response.edit_message(embed=em(),view=vi())   
    select.callback=item_effect_callback
    await interaction.response.edit_message(embed=embed,view=view)
  async def skill_select_callback(interaction:discord.Interaction):
    embed= em()
    con = sqlite3.connect(r"./item.db")
    cur=con.cursor()
    cur.execute(f"SELECT skill_name,skill_mana,skill_hp FROM '''{interaction.user.id}_skill''' WHERE skill_level IS NOT 0 ")
    getSkill=cur.fetchall()
    view = ui.View()
    select= ui.Select(placeholder="스킬 사용",options=[SelectOption(label="돌아가기",value=-1)])
    for i in range(len(getSkill)):
      if mp<getSkill[i][1] or hp<getSkill[i][2]:
        pass
      else:
        select.options.append(SelectOption(label=getSkill[i][0],value=i,description=(f"마나소모:{getSkill[i][1]}" if getSkill[i][1] else "" + f"체력소모:{getSkill[i][2]}" if getSkill[i][2] else "")))
    view.add_item(select)
    async def skill_damage_callback(interaction:discord.Interaction):
      if int(select.values[0]) == -1:
        await interaction.response.edit_message(embed=em(),view=vi())   
      else: 
        global hp
        global mp
        global damage
        global enemy
        enemy=list(enemy)
        con=sqlite3.connect(r"./item.db")
        cur=con.cursor()
        cur.execute(f"SELECT * FROM '''{interaction.user.id}_skill''' LIMIT {select.values[0]},1")
        info = cur.fetchone()
        premyhp=hp
        premydamage=damage.display()
        preenemyhp=enemy[1]
        emojis={}
        preenemydamage=enemy[2]
        li=[]
        for key in effect.keys():
          effect[key]-=1
          emoji=skill.fight(key,0)[0]
          hp,dam,enemy[1],enemy[2],value=skill.fighteffect(key,hp,damage.display(),enemy[1],enemy[2])
          emojis[value]=emoji
          if effect[key]==0:
            li.append(key)
        for i in li:
          del effect[i]
        mp-= info[2]
        hp-= info[3]+enemy[2]
        enemy[1] -= info[4]+ (damage.display()*info[5])
        effect[info[6]]=info[7]
        embed=em()
        embed.add_field(name="**▫▫▫상태▫▫▫**",value="\u200b",inline=False)
        try:
          value
        except NameError:
          value=None
        if not value=="stun":
          embed.add_field(name=f"받은 데미지 {enemy[2]}💔",value='\u200b',inline=False)
        embed.add_field(name=f"준 데미지 {info[4]+ (damage.display()*info[5])}🗡",value="\u200b",inline=False)
        if preenemyhp>enemy[1]+info[4]+ (damage.display()*info[5]):
          embed.add_field(name=f'준 데미지 {preenemyhp-(enemy[2]+info[4]+ (damage.display()*info[5]))}{emojis[value]}',value="\u200b",inline=False)
        embed.set_thumbnail(url=info[9])
        await end(interaction)
        if not interaction.response.is_done():
          await interaction.response.edit_message(embed=embed,view=vi())
    select.callback=skill_damage_callback
    await interaction.response.edit_message(embed=embed,view=view)

  async def attack_callback(interaction:discord.Interaction):
    global hp
    global damage
    global enemy
    global mp
    premyhp=hp
    premydamage=damage
    preenemyhp=enemy[1]
    emojis={}
    preenemydamage=enemy[2]
    lists=[]
    dam=0
    enemy=list(enemy)
    for key in effect.keys():
      effect[key]-=1
      emoji=skill.fight(key,0)[0]
      hp,dam,enemy[1],enemy[2],value=skill.fighteffect(key,hp,damage.display(),enemy[1],enemy[2])
      emojis[value]=emoji
      if effect[key]==0:
        lists.append(key)
    for i in lists:
      del effect[i]
    d=damage.critical()
    hp-=enemy[2]
    enemy[1]-=d[0]
    embed=em()
    embed.add_field(name="**▫▫▫상태▫▫▫**",value="\u200b",inline=False)
    try:
      value
    except NameError:
      value=None
    if not value=="stun":
      embed.add_field(name=f"받은 데미지 {enemy[2]}💔",value='\u200b',inline=False)
    name=f"준 데미지 {d[0]}🗡"
    if d[1]:
      name=f"준 데미지 **CRITICAL** {d[0]}🗡"
    embed.add_field(name=name,value='\u200b',inline=False)
    
    if dam!=0 and value=="damage":
      embed.add_field(name=f'준 데미지 {dam}{emojis[value]}',value="\u200b",inline=False)
    await end(interaction)
    if not interaction.response.is_done():
      await interaction.response.edit_message(embed=embed)
  async def end(interaction:discord.Interaction):
    if hp<=0:
      dungeon_dic[interaction.user.id]=False
      embed=discord.Embed(title="사망")
      embed.set_image(url="https://img.freepik.com/free-vector/game-over-in-retro-pixel-art-design-glitch-and-noise-style-isolated-on-white-background-concept-of-level-final-in-virtual-gaming-or-classic-user-interface-for-online-videogames-vector-illustration_342166-224.jpg?w=740")
      await interaction.response.edit_message(embed=embed,view=None)
    if enemy[1]<=0:
      embed=discord.Embed(title="전투 보상")
      button=ui.Button(label="다시 탐험",style=ButtonStyle.green,disabled=True)
      button.callback=dungeon
      view=ui.View()
      view.add_item(button)
      reward=Reward(층,interaction.user.id,enemy[5],enemy[4])
      etcname,etcamount=reward.etc(enemy)
      usename,useamount=reward.use(enemy)
      rewardWeapon=reward.weapon()
      reward.defualt()
      rewardWear=reward.wear()
      defualt=Default(interaction.user.id)
      level=defualt.isLevel()

      if level:
        embed.add_field(name=f"**{level} 레벨** 달성!",value="\u200b",inline=False)

      if rewardWeapon:
        embed.add_field(name=f"[무기] **{rewardWeapon}**를 획득했습니다.",value='\u200b',inline=False)
      if rewardWear:
        embed.add_field(name=f"[장비] **{rewardWear}**를 획득했습니다.",value='\u200b',inline=False)
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/988424121878741022/989064226083590145/chest.png")
      embed.add_field(name=f"**{enemy[4]}골드 {enemy[5]}경험치**를 획득했습니다.",value="\u200b",inline=False)
      for i in range(len(etcname)):
        embed.add_field(name=f"[기타] **{etcname[i]} {etcamount[i]}개**를 획득했습니다.",value='\u200b',inline=False)
      for i in range(len(usename)):
        embed.add_field(name=f"[소비] **{usename[i]} {useamount[i]}개**를 획득했습니다.",value='\u200b',inline=False)
      dungeon_dic[interaction.user.id]=False
      await interaction.response.edit_message(embed=embed,view=view)
  await interaction.response.send_message(embed=em(),view=vi(),ephemeral=True)
@tree.command(guild= discord.Object(id=955246008923742209),name="가이드", description="ㅇㅇ")
async def Guide(interaction:discord.Interaction):
  embed=discord.Embed(title="MOTD")
  embed.add_field(name="ㅇㅇ",value="ㅇㅇ")
  await interaction.response.send_message(content=interaction.user.mention,embed=embed,ephemeral=True)

@tree.command(guild= discord.Object(id=955246008923742209),name="인벤토리", description="인벤토리를 엽니다.")
async def Inventory(interaction:discord.Interaction, 종류:Inventory):
  async def inventory_callback(interaction:discord.Interaction):
    embed=discord.Embed(title=f"{종류.name} 인벤토리")
    inventory=ItemInventory(interaction.user.id,종류.value)
    item=inventory.item()
    view = ui.View()
    list=["_use","_etc","_cash"]
    if len(inventory.item())==0:
      embed.add_field(name="아이템이 없어요!",value="\u200b")
      return await interaction.response.edit_message(embed=embed,view=None)
    if inventory.value in list:
      j=0
      for i in range(len(inventory.item())):
        if item[i-j][2]==0:
          item.pop(i-j)
          j+=1
    if not item:
      embed.add_field(name="아이템이 없어요!",value="\u200b")
      return await interaction.response.edit_message(embed=embed,view=None)
    if inventory.value == "_weapon" or inventory.value=="_wear":
      a=["_weapon","_wear"]
      var="(착용중)"
      empty=""
      options=[SelectOption(label=(f"+{item[i][1]} {item[i][0]} {var if item[i][13+a.index(inventory.value)] else empty}") ,value =i) for i in range(len(item))]
    else:
      var="거래가능"
      val="거래불가"
      options=[SelectOption(label=(f"({item[i][0]}) {item[i][1]} ({var if item[i][4] else val})") ,value =i )for i in range(len(item))]
    select = ui.Select(placeholder="원하는 아이템을 골라주세요.",options=options)
    view.add_item(select)

    async def equip_callback(interaction:discord.Interaction):
      con=sqlite3.connect(r"./item.db")
      cur=con.cursor()
      if inventory.value=="_weapon":
        cur.execute(f"UPDATE '''{interaction.user.id}{inventory.value}''' SET wear = 0 WHERE wear = 1")
        cur.execute(f"UPDATE '''{interaction.user.id}{inventory.value}''' SET wear = 1 WHERE rowid in (SELECT rowid FROM '''{interaction.user.id}{inventory.value}'''LIMIT {select.values[0]},1)")
      elif inventory.value=="_wear":  
        cur.execute(f"UPDATE '''{interaction.user.id}{inventory.value}''' SET wear = 0 WHERE wear = 1 AND part = {item[int(select.values[0])][15]}")
        cur.execute(f"UPDATE '''{interaction.user.id}{inventory.value}''' SET wear = 1 WHERE rowid in (SELECT rowid FROM '''{interaction.user.id}{inventory.value}'''LIMIT {select.values[0]},1)")
      con.commit()
      embed.set_footer(text="성공적으로 아이템을 착용했습니다.")
      view=ui.View()
      back = ui.Button(style=ButtonStyle.primary,emoji="↩",label="돌아가기")
      view.add_item(back)
      back.callback=inventory_callback
      await interaction.response.edit_message(embed=embed,view=view)
    async def select_callback(interaction:discord.Interaction):
      info,true,url,tem,gap=inventory.display(item[int(select.values[0])])
      embed.set_thumbnail(url=url)
      view = ui.View()
      if inventory.value == "_weapon" or inventory.value=="_wear":
        for i in range(len(tem)):
          embed.add_field(name=info[i],value=f"{tem[i]} {gap[i] if gap[i] else empty}",inline=true[i])
        con=sqlite3.connect(r'./rpg.db')
        cur=con.cursor()
        cur.execute("SELECT level FROM user_data WHERE id = ?",(interaction.user.id,))
        level = cur.fetchone()[0]
        equip = ui.Button(style=ButtonStyle.green,emoji="🛡",disabled=(False if level>=tem[3] else True),label=("착용하기" if level>=tem[3] else "레벨이 낮습니다."))
        back = ui.Button(style=ButtonStyle.primary,emoji="↩",label="돌아가기")
        view.add_item(equip)
        view.add_item(back)
        back.callback=inventory_callback
        equip.callback=equip_callback
      else:
        view=ui.View()
        back = ui.Button(style=ButtonStyle.primary,emoji="↩",label="돌아가기")
        view.add_item(back)
        back.callback=inventory_callback
        for i in range(len(tem)):
          embed.add_field(name=info[i],value=tem[i],inline=true[i])
      await interaction.response.edit_message(embed=embed,view=view)
    select.callback=select_callback
    await interaction.response.edit_message(embed=embed,view=view)
  view=ui.View()
  button=ui.Button(style=ButtonStyle.danger,label="인벤토리 보러가기")  
  view.add_item(button)
  button.callback=inventory_callback
  await interaction.response.send_message(view=view,ephemeral=True)



#@tree.command(guild= discord.Object(id=955246008923742209),name="전직", description="전직을 할수 있습니다.")
@tree.command(guild= discord.Object(id=955246008923742209),name="스킬", description="스킬을 찍을수 있습니다.")
async def 스킬(interaction:discord.Interaction):
  skill=Skill(interaction.user.id)
  skill.isSkill()
  view = ui.View()
  select=ui.Select(placeholder="원하는 스킬을 골라주세요.",options=[])
  for i in range(len(skill.select())):
    select.options.append(SelectOption(label=(f"(Lv. {skill.select()[i][3]}) {skill.select()[i][0]} ({skill.select()[i][1]}/{skill.select()[i][2]})"),value=i))
  view.add_item(select)
  def func():
    embed=discord.Embed(title="스킬 정보")
    info=list(skill.display(select.values[0]))
    info[8]=Class(info[8]).display()
    info[6]=skillModify(interaction.user.id).effect(info[6])
    name=['스킬명',"",'마나소모량','체력소모량','스킬데미지','계수','효과','지속시간','직업',"",'스킬포인트','스킬레벨',"최대레벨","요구레벨"]
    con=sqlite3.connect(r"./rpg.db")
    cur=con.cursor()
    cur.execute("SELECT skill_point FROM user_stat WHERE id = ?",(interaction.user.id,))
    point=cur.fetchone()[0]
    for i in range(len(info)):
      if i == 6:
        embed.add_field(name="\u200b",value="\u200b")
      if i ==11:
        embed.add_field(name="\u200b",value="\u200b")
        embed.add_field(name="\u200b",value="\u200b")
      if i ==9:
        embed.set_thumbnail(url=info[i])
      elif i==1:  
        pass
      else:
        embed.add_field(name=name[i],value=info[i])
    embed.set_footer(text=f"남은 스킬포인트: {point}")
    view=ui.View()
    button=ui.Button(style=ButtonStyle.green,label="스킬레벨업⬆",disabled=skill.require(select.values[0]))
    view.add_item(button)
    button.callback=button_callback
    return embed,view
  async def button_callback(interaction:discord.Interaction):
    modify=skillModify(interaction.user.id)
    info=skill.display(select.values[0])
    modify.upgrade(info[1],info[11],info[10])    
    await interaction.response.edit_message(embed=func()[0],view=func()[1])
  async def select_callback(interaction:discord.Interaction):

    await interaction.response.edit_message(embed=func()[0],view=func()[1])
  select.callback=select_callback
  await interaction.response.send_message(view=view,ephemeral=True)

@tree.command(guild= discord.Object(id=955246008923742209),name="계정삭제", description="계정과 관련된 모든 데이터가 삭제됩니다.")
async def Cut(interaction:discord.Interaction,sure:bool):
  if sure:
    view = ui.View()
    button=ui.Button(label="네.",style=ButtonStyle.danger)
    view.add_item(button)
    async def button_callback(interaction:discord.Interaction):
      con=sqlite3.connect(r'./rpg.db')
      cur=con.cursor()      
      cur.execute("DELETE FROM user_stat WHERE id = ? ",(interaction.user.id,),)
      cur.execute("DELETE FROM user_data WHERE id = ? ",(interaction.user.id,),)
      li=["weapon","wear","etc","use","cash"]
      for i in li:
        cur.execute(f"DELETE FROM trade_{i} WHERE id = ?",(interaction.user.id,))
      con.commit()  
      con=sqlite3.connect(r"./item.db")
      cur=con.cursor()

      li.append("skill")
      for i in li:
        cur.execute(f"DROP TABLE '''{interaction.user.id}_{i}'''")
      con.commit()
      await interaction.response.edit_message(content="삭제되었습니다",view=None)
    button.callback=button_callback
    await interaction.response.send_message(content="확실합니까?",view=view,ephemeral=True) 
@tree.command(guild= discord.Object(id=955246008923742209),name="건의하기", description="건의를 할수있습니다.")
async def modal(interaction:discord.Interaction):
  await interaction.response.send_modal(reportModal())
@tree.command(guild= discord.Object(id=955246008923742209),name="데이터", description="..")
async def Command(interaction:discord.Interaction, code:str):
  if code=="아잉아잉0325":
    #test1=Reward(1,interaction.user.id,0,0)
    #test2=Reward(2,interaction.user.id,0,0)  
    #default=Default(interaction.user.id)
    #default.isItem()
    con=sqlite3.connect(r"./rpg.db")
    cur=con.cursor()
    #cur.execute("INSERT INTO etc VALUES(?,?,?,?,?,?)",(2,'강화의 서',0,50,0,'https://cdn.discordapp.com/attachments/884063587344207904/949085121158447155/60bff62ca078a941.png'))
    #cur.execute("CREATE TABLE IF NOT EXISTS skill(skill_name TEXT, skill_id INTEGER, skill_mana INTEGER, skill_hp	INTEGER, skill_damage INTEGER, skill_calculate 	INTEGER, skill_effect TEXT, skill_turn INTEGER, skill_class INTEGER, skill_image TEXT, skill_point INTEGER, skill_level INTEGER, skill_maxlevel INTEGER)")
    #cur.execute("INSERT INTO skill VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",("찌르기",1,20,0,50,1,'blood',2,0,None,1,0,1))
    con.commit()
client.run(os.environ['token'])