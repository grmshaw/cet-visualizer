<html>
    <head>
        <title>CET-4 Visualization</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="shortcut icon" type="image/x-icon" href="/static/favicon.png">
        <link rel="stylesheet" href="/static/index.css">
    </head>
    <body>
        <div class="container">
            <h1>CET-4 Visualization</h1>
            <div>
                <p>1. 各项分数名称需要是：<strong>写作</strong>（或作文）、听力、阅读、翻译，且<strong>顺序</strong>也保持一致</p>
                <p>2. 无隐藏单元行，无隐藏表头</p>
                <p>3. 所有打分为且仅为<strong>数字</strong>，如果分值包含 “11 分” 这样的文字内容，程序将报错</p>
            </div>
            <form action="/upload" method="post" enctype="multipart/form-data" accept-charset="UTF-8">
                <input type="file" name="file" accept=".xlsx, .xls" size="1048576">
                <input class="classname"  type="text" name="classname" placeholder="请输入班级名称" required>
                <input type="submit" value="Upload">
            </form>
        </div>
        <footer>
            <p>Made with &hearts; by Cyan & <a href="https://grm.sh" target="_blank">Graham</a></p>
        </footer>
    </body>
</html>
