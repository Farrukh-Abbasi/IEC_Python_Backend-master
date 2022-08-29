
student = {
    "date": "January, 1st 2022",
    "name": "John Doe",
    "courseName": "Web Development"
}

certificateHtml = '''

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
<div class="mainContainer" id="mainContainer2">

        <!-- <img src="" class="" alt="Certificate" id="certificateImgTage" /> -->
        <div id="certificateImage" class="imgContainer">
            <h4 class="date">{}</h4>
            <h1 class="name">{}</h1>

            <h2 class="courseName">{}</h2>
        </div>


    </div>

</body>

</html>
'''.format(student['date'], student['name'], student['courseName'])

certificateCss = '''
body {
            background-color: white;
        }

        #mainContainer2 {
            opacity: 1;
        }

        #certificateImgTage {
            width: 100%;
            height: 100%;
            position: absolute;
        }

        .mainContainer {
            width: 100%;
            height: 100%;

        }

        .imgContainer {
            position: absolute;

            background-image: url('certificate.svg');
            background-repeat: no-repeat;
            height: 786px;
            width: 1066px;
            background-color: white;
        }

        .date {
            font-family: montserrat;
            font-size: 12pt;
            letter-spacing: 1px;
            color: #4E87B3;
            position: absolute;
            top: 29%;
            left: 14%;
        }

        .name {
            font-family: montserrat;
            white-space: nowrap;
            overflow: visible;
            font-size: 34pt;
            letter-spacing: 2px;
            color: #434340;
            position: absolute;
            top: 38%;
            left: 14%;

        }

        .courseName {
            font-family: montserrat;

            font-size: 16pt;
            letter-spacing: 3px;
            color: #305775;
            position: absolute;
            top: 51.8%;
            left: 14%;
        }
'''
