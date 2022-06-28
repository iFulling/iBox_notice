const mysql = require('mysql');
const express = require('express');
const dayjs = require('dayjs');
const app = express();

app.use(express.static('../server'));

const conn = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'lKnT5ndIKhHsQaJ4',
    port: '3306',
    database: 'noticeapp',
});
conn.connect();

setInterval(function () {
    conn.query('SELECT 1', (error, results, fields) => {
        if (error) return console.log(error);
        console.log("数据库准备完成");
    });
  }, 3600000);

app.post('/reg', (request, response) => {
    conn.query(
        "SELECT * from notice_user where userName = '" + request.query['userName'] + "'",
        (error, results, fields) => {
            if (error)  return console.log(error);
            results = JSON.stringify(results);
            let regTime = dayjs(Date.now()).format('YYYY-MM-DD HH:mm:ss')
            if (results === '[]') {
                conn.query('INSERT INTO notice_user(userName,userPwd,regTime) VALUES("' + request.query['userName'] + '", "' + request.query['userPwd'] + '", "' + regTime + '");');
                response.send({ status: 200, content: '注册成功，快去登陆吧！' });
                console.log(regTime, request.get("Host") + ' 注册了账号：' + request.query['userName']);
            } else {
                response.send({ status: 400, content: '用户名已存在！' });
            }
        }
    );
});

app.post('/login', (request, response) => {
    queryUserName = request.query['userName']
    queryKeyId = request.query['keyID']
    let regTime = dayjs(Date.now()).format('YYYY-MM-DD HH:mm:ss')
        // # 验证是否注册过
    conn.query("SELECT * from notice_user where userName = '" + queryUserName + "'",
        (error, results, fields) => {
            if (error)  return console.log(error);
            results = JSON.stringify(results);
            if (results !== '[]') {

                // 验证密码是否正确
                conn.query("SELECT userPwd from notice_user where userName = '" + queryUserName + "'",
                    (error, results, fields) => {
                        if (error)  return console.log(error);
                        let userPwd = results[0].userPwd;
                        if (userPwd === request.query['userPwd']) {

                            // 如果正确，验证密钥存在且 是否使用过 select keyID from notice_key where userName = "231312"
                            conn.query("SELECT * from notice_key where keyID = '" + request.query['keyID'] + "'",
                                (error, results, fields) => {
                                    if (error)  return console.log(error);
                                    // console.log(results);
                                    if (JSON.stringify(results) !== "[]") {
                                        if (!results[0].userName) {
                                            // 没有使用过，则加入现在的时间戳
                                            conn.query('UPDATE notice_key SET userName = "' + queryUserName + '", startTime = now(), stopTime=date_add(startTime, interval notice_key.days day) WHERE keyID = "' + queryKeyId + '"')
                                            return response.send({ status: 200, content: '登陆成功', userName: queryUserName });
                                        } else {
                                            // 判断是否是绑定用户
                                            if (results[0].userName === queryUserName) {
                                                // 判断是否过期
                                                if (Date.now() <= Date.parse(results[0].stopTime)) {
                                                    return response.send({ status: 200, content: '登陆成功', userName: queryUserName });
                                                } else {
                                                    return response.send({ status: 400, content: '密钥已过期，请联系管理员。' });
                                                }
                                            }
                                            return response.send({ status: 400, content: '密钥已被使用' });
                                        }
                                    } else {
                                        return response.send({ status: 400, content: '密钥输入错误' });
                                    }
                                }
                            )
                        } else {
                            return response.send({ status: 400, content: '密码错误' });
                        }
                    })
            } else {
                return response.send({ status: 400, content: '该账号尚未注册' });
            }
            // console.log(regTime, request.get("Host") + ' 注册了账号：' + request.query['userName']);
        })
});

app.all("/context", (request, response) => {
    // console.log(request.query['userName']);

    conn.query("SELECT * from notice_user where notice_user.userName = '" + request.query['userName'] + "'",
        (error, results, fields) => {
            if (error)  return console.log(error);
            console.log(results);
            return response.send({
                status: 200,
                emails: results[0].emails,
                sendEmail: results[0].sendEmail,
                sendKey: results[0].sendKey,
                delayTime: results[0].delayTime,
            });
        })
})

app.post("/close", (request, response) => {
    emails = JSON.stringify(request.query['emails'])
        // console.log(request.query);
        // console.log("update notice_user set emails='" + emails + "', sendEmail='" + request.query['sendEmail'] + "', sendKey='" + request.query['sendKey'] + "', delayTime='" + request.query['delayTime'] + "' where userName='" + request.query['userName'] + "'");
    conn.query("update notice_user set emails='" + emails + "', sendEmail='" + request.query['sendEmail'] + "', sendKey='" + request.query['sendKey'] + "', delayTime='" + request.query['delayTime'] + "' where userName='" + request.query['userName'] + "'",
        (error, results, fields) => {
            if (error)  return console.log(error);
            response.send("666")
        })
})
app.get('/checknet', (request, response) => {
    return response.send({ status: 200, content: 'success', level: 1.2 });
})

app.get("/update", (request, response) => {
    // return response.sendFile('public/README.md')
    return response.sendFile('C:/Users/Administrator/Desktop/KOA_SERVER/iBox公告检测.exe')
})

app.listen(3000, () => {
    console.log('3000..');
});