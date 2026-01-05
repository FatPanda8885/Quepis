from flask import Flask, redirect, url_for, request, render_template, abort, flash, get_flashed_messages, session

import config
config.setup()
CONFIG = config.get_config()

import database
import unban
import log

app = Flask(__name__)
app.secret_key = 'ewq23521fg13w321tgf241'# 必须设置 secret_key 才能使用 session
log.setup()
database.setup()
unban.setup()
app.secret_key = CONFIG.get('web', 'secret_key')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input:
            uuid = database.match_uuid(user_input)
            ban = database.search_uuid(uuid)

            # 错误判断：直接返回首页并提示错误信息
            if uuid is None or not uuid:
                flash("该用户不存在或没有被封禁", "error")
                return redirect(url_for('index'))

            if ban[0] == False:  # 没有被封禁
                flash("该用户不存在或没有被封禁", "error")
                return redirect(url_for('index'))

            # 只有符合解封条件才进入 submit 页面
            result = {"uuid": uuid, "ban": ban[1]}
            session['submit_data'] = {
                'result': result,
                'username': user_input
            }

            return redirect(url_for('submit'))

        # 如果输入为空
        return render_template('index.html')

    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    # 从 session 获取数据
    submit_data = session.get('submit_data')

    if not submit_data:
        abort(400, description="缺少必要的会话数据")

    result = submit_data['result']
    username = submit_data['username']

    # 从 result 中提取 ban 字段
    ban = result.get('ban') if isinstance(result, dict) else None

    # 检查是否符合解封条件（注意参数顺序修正：check_reason(ban)）
    can_unban = False
    if ban:
        can_unban = unban.check_reason(ban)

    # 处理提交请求
    if request.method == 'POST':
        if can_unban:
            success = unban.unban(username)
            if success:
                flash("用户已成功解封！", "success")
                return redirect(url_for('index'))  # 成功，跳转到首页
            else:
                flash("解封失败，请检查服务器连接。", "error")
        else:
            flash("该用户不符合解封条件。", "error")

        return redirect(url_for('submit')) # 失败，刷新提交页面

    return render_template('submit.html', result=result, username=username, can_unban=can_unban)


if __name__ == '__main__':
    app.run(threaded=True, debug=False)
