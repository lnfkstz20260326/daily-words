import json

# 读取素材库
with open('content_backup/content_backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("开始修复素材库...")
print("=" * 60)

# 常见例句模板（用于补充缺失的例句）
example_templates = {
    # fly相关
    "fly": ("Birds can fly.", "鸟会飞。"),
    # throw相关
    "throw": ("Throw the ball.", "扔球。"),
    # catch相关
    "catch": ("Catch the ball!", "接住球！"),
    # kick相关
    "kick": ("Kick the ball.", "踢球。"),
    # hit相关
    "hit": ("Hit the ball.", "击球。"),
    # bowl相关
    "bowl": ("This is a nice bowl.", "这是一个漂亮的碗。"),
    # cup相关
    "cup": ("I want a cup of tea.", "我想要一杯茶。"),
    # walk相关
    "walk": ("I walk to school.", "我走路去学校。"),
    # near相关
    "near": ("The park is near my home.", "公园在我家附近。"),
    # test相关
    "test": ("We have a test today.", "我们今天有考试。"),
    # sentence相关
    "sentence": ("Read this sentence.", "读这个句子。"),
    # story相关
    "story": ("Tell me a story.", "给我讲个故事。"),
    # hallway相关
    "hallway": ("Walk down the hallway.", "走过走廊。"),
    # ground相关
    "ground": ("Sit on the ground.", "坐在地上。"),
    # snack相关
    "snack": ("I want a snack.", "我想吃零食。"),
    # chocolate相关
    "chocolate": ("I like chocolate.", "我喜欢巧克力。"),
    # spoon相关
    "spoon": ("Use the spoon.", "用勺子。"),
    # knife相关
    "knife": ("Be careful with the knife.", "小心刀。"),
    # ball相关
    "ball": ("Throw the ball.", "扔球。"),
    # exercise相关
    "exercise": ("Do exercise every day.", "每天做运动。"),
    # storybook相关
    "storybook": ("Read the storybook.", "读故事书。"),
    # magazine相关
    "magazine": ("Read this magazine.", "读这本杂志。"),
    # librarian相关
    "librarian": ("The librarian is kind.", "图书管理员很和蔼。"),
    # mom相关
    "mom": ("I love my mom.", "我爱妈妈。"),
    # dad相关
    "dad": ("My dad is tall.", "我爸爸很高。"),
    # egg相关
    "egg": ("I like eggs.", "我喜欢鸡蛋。"),
    # rice相关
    "rice": ("We eat rice.", "我们吃米饭。"),
    # noodles相关
    "noodles": ("I like noodles.", "我喜欢面条。"),
    # fruit相关
    "fruit": ("Eat more fruit.", "多吃水果。"),
    # apple相关
    "apple": ("An apple a day.", "每天一个苹果。"),
    # kitchen相关
    "kitchen": ("Mom is in the kitchen.", "妈妈在厨房。"),
    # plate相关
    "plate": ("Put it on the plate.", "把它放在盘子上。"),
    # bus相关
    "bus": ("Take the bus.", "乘公交车。"),
    # bike相关
    "bike": ("I ride a bike.", "我骑自行车。"),
    # street相关
    "street": ("Our school is on this street.", "我们学校在这条街上。"),
    # traffic相关
    "traffic": ("The traffic is heavy.", "交通很拥挤。"),
    # light相关
    "light": ("Turn off the light.", "关灯。"),
    # wait相关
    "wait": ("Please wait.", "请等一下。"),
    # minute相关
    "minute": ("It takes 10 minutes.", "需要10分钟。"),
    # far相关
    "far": ("It is not far.", "不远。"),
    # teacher相关
    "teacher": ("Our teacher is kind.", "我们的老师很和蔼。"),
    # principal相关
    "principal": ("The principal is nice.", "校长很友好。"),
    # blackboard相关
    "blackboard": ("Write on the blackboard.", "在黑板上写字。"),
    # chalk相关
    "chalk": ("Pass me the chalk.", "把粉笔递给我。"),
    # read相关
    "read": ("I like to read.", "我喜欢阅读。"),
    # write相关
    "write": ("Write your name.", "写你的名字。"),
    # spell相关
    "spell": ("Spell the word.", "拼写这个单词。"),
    # forget相关
    "forget": ("Don't forget.", "别忘记。"),
    # page相关
    "page": ("Turn to page 10.", "翻到第10页。"),
    # picture相关
    "picture": ("Draw a picture.", "画一幅画。"),
    # play相关
    "play": ("We play games.", "我们玩游戏。"),
    # talk相关
    "talk": ("Let's talk.", "我们聊聊天吧。"),
    # run相关
    "run": ("Don't run.", "不要跑。"),
    # jump相关
    "jump": ("Jump high.", "跳高点。"),
    # open相关
    "open": ("Open the window.", "打开窗户。"),
    # close相关
    "close": ("Close the door.", "关门。"),
    # toilet相关
    "toilet": ("Where is the toilet?", "洗手间在哪里？"),
    # drink相关
    "drink": ("I want to drink.", "我想喝水。"),
    # candy相关
    "candy": ("Don't eat too much candy.", "不要吃太多糖果。"),
    # pass相关
    "pass": ("Pass the dishes.", "传递盘子。"),
    # meal相关
    "meal": ("This is a nice meal.", "这是一顿美餐。"),
}

fix_count = 0
empty_count = 0
duplicate_count = 0

for date, words in data.items():
    new_words = []

    for i, word in enumerate(words):
        word_en = word.get('word_en', '').strip()
        example_en = word.get('example_en', '').strip()
        example_zh = word.get('example_zh', '').strip()

        # 检查是否与上一个词重复（忽略大小写）
        is_duplicate = False
        if i > 0:
            prev_word_en = words[i-1].get('word_en', '').strip()
            prev_example = words[i-1].get('example_en', '').strip()
            if word_en.lower() == prev_word_en.lower() and example_en.lower() == prev_example.lower():
                is_duplicate = True
                duplicate_count += 1

        if is_duplicate:
            continue  # 跳过重复的词条

        # 检查例句是否为空
        if not example_en or not example_zh:
            # 尝试使用模板
            word_lower = word_en.lower()
            if word_lower in example_templates:
                word['example_en'] = example_templates[word_lower][0]
                word['example_zh'] = example_templates[word_lower][1]
                empty_count += 1
                fix_count += 1

        new_words.append(word)

    data[date] = new_words

print(f"\n修复完成！")
print(f"  - 去除重复词条：{duplicate_count} 个")
print(f"  - 补充缺失例句：{empty_count} 个")
print(f"  - 总修复数：{fix_count} 个")

# 保存修复后的素材库
with open('content_backup/content_backup_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n已保存到 content_backup_fixed.json")
print("请验证后再替换原文件。")
