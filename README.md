<div align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80526256-7015cf80-89cd-11ea-8ffa-ad0234451773.PNG">
</div>
<br>
<br>

<p align="center">
<a href="https://opensource.org/licenses/Apache-2.0"><img alt="License" src="https://img.shields.io/badge/License-Apache%202.0-blue.svg"/></a>
<a href="https://www.djangoproject.com/"><img alt="django" src="https://img.shields.io/badge/django-3.0-green.svg"/></a>
<a href="https://www.djangoproject.com/"><img alt="djangorestframework" src="https://img.shields.io/badge/djangorestframework-3.10.3-brightgreen.svg?style=flat"/></a>
<a href="https://opencv.org/"><img alt="openCV" src="https://img.shields.io/badge/OpenCV-4.3.0-red.svg"/></a>
<br>
<p>
  
<h2>Motivation</h2></br>
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80531155-174a3500-89d5-11ea-82a7-27d428533fd1.gif">
</p>
<br><br>
<p>With the recent development of the Internet and streaming services, more Internet lectures are being created, and demand is also increasing.
However, these Internet lectures continue to have a similar system, and there are still things that cause discomfort by listening in the system.
First, the Internet lecture is a structure in which the lecturer and the viewer cannot interact.
Viewers have a hard time knowing where they haven't seen if they haven't focused on the lecture.
Even video providers can't tell which part of their video wasn't responding well and where the viewers had a good concentration rate.
So, we developed a READ solution, Reaction evaluation & aggregation data, to solve this problem.
It is a process divided into Reaction evaluation part that judges user's concentration and Aggregation data part that collects viewer's data and analyzes it to give feedback to video providers.
Through this solution, video viewers can analyze the concentration level of the video to compensate for the lack of concentration and provide motivation to increase concentration.
Video providers can also see the concentration of viewers, grasp the strengths and weaknesses of their video, and make efforts to improve the video.
  </p>
<br>

<h2>Install</h2></br>

See the [Python install guide](https://www.python.org/downloads/) for the
[pip package](https://www.python.org/downloads/pip) to install the necessary modules to run basic Python functions.
```
$ pip install scikit-learn
```
```
$ pip install numpy
```
```
$ pip install pandas
```
<br>
The OpenCV module can be installed via pip.

```
$ python -m pip install opencv-python
```
<br>
Make sure opencv is installed properly.

```
 import cv2
print(cv2.__version__)
```
<br>
Install to complement the poor usability of OpenCV.

```
$ pip install dlib
```
```
$ pip install imutils
```
<br>
Use GridSearchCV to find the best parameters.

```
$ pip install xgboost
```
<br>

[Download](https://pjreddie.com/darknet/yolo/) the yolo-coco file in read\analyzer for real-time object detection.

<br>
<h2>Usage</h2></br>

It is a platform that provides video and utilizes user information and analyzes it using a web server and a pro-end.
We installed these two because we used bootstrap as django and frontend as backend.
<br>
<h4>bootstrap</h4>
Since we created a web page with bootstrap, you can use bootstrap if you want to [change it to a web page](https://getbootstrap.com/docs/3.3/getting-started/) of your choice.
<br>
<h4>Django</h4>
Python 3.x version or higher is possible, so check the version.

```
$ python --version
$ pip install django
$ pip3 install djangorestframework
```
<br>
To run the server, run a cmd window in the part of manage.py in the READ file.

```
$ manage.py migrate
$ python manage.py runservero
```
<br>
<div align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80536016-af97e800-89dc-11ea-885c-38ffc93e3825.jpg">
</div><br>
After running the server, proceed to membership registration and store the membership information on the DB.

```
$ manage.py migrate --run-syncdb
```
<br>
 
In order to distinguish between video providers and viewers, they are classified by level in Django administration.<br>

<br>
<div align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80536029-b45c9c00-89dc-11ea-96b9-c0a4f03eb271.PNG" width="50%">
  </div><br>
 
Register videos to be provided to video viewers.
The code is in register_video.html.
If you click the 'Register' button, the video will be saved in a file called media.

```

<!--- add Video  ---->
<section id="videoAdd">
    <div class="container">
    <h3 class="title text-center">ADD VIDEO</h3>
    <br>
    <div class="row mt-5">
        <div class="col-12" role="alert">
            {{ error }}
        </div>
        <br><br>
        <div class="col-12">
            <form method="POST" action="." enctype="multipart/form-data">
                {% csrf_token %}
                {% for field in form %}
                <div class="form-group">
                    <label for="{{ field.id_for_label }}"> {{ field.label }}</label>
                    {% ifequal field.name 'description' %}
                    <textarea class="form-control" name="{{ field.name }}" id="{{ field.id_for_label }}"></textarea>
                    {% else %}
                    <input type="{{ field.field.widget.input_type }}" class="form-control" id="{{ field.id_for_label }}"
                        placeholder="{{ field.label }}" name="{{ field.name }}" />
                    {% endifequal %}
                </div>
                {% if field.errors %}
                <div class="alert alert-danger" role="alert">
                        {{ field.errors }}
                </div>
                {% endif %}
                {% endfor %}
                <div class="d-flex justify-content-end">
                    <button type="submit" class="btn btn-primary">등록</button>
                </div>
                <p></p>
```
<br>
While watching video in real time, it is captured and uploaded at regular intervals.
At this time, Upload images using ‘POST’ method Per 𝒕 𝒔𝒆𝒄
If you change the second parameter to setTimeout function, you can adjust this fixed time to upload photos.


```
 // ajax (POST)
  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "http://127.0.0.1:8000/upload/",
    "method": "POST",
    "processData": false,
    "contentType": false,
    "mimeType": "multipart/form-data",
    "data": form,
    success: function(){
      $('.result').html();
    },
    complete: function(){
      // 10 sec --> upload
      // If change, must change face_analyzer.py --> duration 264
      timeout = setTimeout(captureWebcam, 10000);
    }
  }

  $.ajax(settings).done(function (response) {
    console.log(response);
  });
}
```
<br>
Using gaze detection, object detection, and face detection on images uploaded during video viewing through machine learning and opencv
Train to make a model.
Build the model using GridSearchCV to find the best parameters.


```
params = {
        'min_child_weight': [1, 5, 10],
        'gamma': [0.5, 1, 1.5, 2, 5],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.6, 0.8, 1.0],
        'max_depth': [3, 4, 5]
        }
xgb = XGBClassifier(learning_rate=0.02, n_estimators=600, objective='binary:logistic',silent=True, nthread=1)
model = GridSearchCV(xgb, params, refit=True)
model.fit(X_train, y_train)
y_predict = pd.Series(model.predict(X_test))

```
<br>
Save the model in json format.
(0: concentrate, 1: Not concentrate)

<br>

The concentration value stored in json format is displayed using the dashboard for easy viewing by the user.
You can see where you are not paying attention.<br>


<div align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80542066-4ff30a00-89e7-11ea-9778-1dae028af9b7.PNG" width="80%">
</div>
<br>

It is a dashboard to show the concentration of each video time.

<br>

```

for(var i = 0; i < time.length; i++){
  switch(time[i]){
    case 0: // Concentrate
      graph_data[i] = {
        type: "stackedBar",
        color: "#4157fa",
        toolTipContent: "{label}<b>{name}:</b> {y}",
        name: "Concen O",
        dataPoints: [{ y: 10 }]
      };
      break;
    case 1: // Don't concentrate
      graph_data[i] = {
        type: "stackedBar",
        color: "#F15628",
        toolTipContent: "{label}<b>{name}:</b> {y}",
        name: "Concen X",
        dataPoints: [{ y: 10 }]
      }
      break;
    case 2: // Don't concentrate
      graph_data[i] = {
        type: "stackedBar",
        color: "#F15628",
        toolTipContent: "{label}<b>{name}:</b> {y}",
        name: "Concen X",
        dataPoints: [{ y: 10 }]
      }
      break;
  }
}
```
<br>

<div align="center">
  <img src="https://user-images.githubusercontent.com/44631215/80542060-4ec1dd00-89e7-11ea-91f1-f12fbfa34e7f.PNG" width="35%">
</div>
<br>

It is a dashboard to show the overall concentration of images.

<br>

```
var piechart = new CanvasJS.Chart("piechartContainer", {
  animationEnabled: true,
  data: [{
    type: "pie",
    startAngle: 240,
    yValueFormatString: "##0.00\"%\"",
    indexLabel: "{label} {y}",
    dataPoints: [
      {y: counts[0], label: "Concen O", color: "#4157fa"},
      {y: counts[1] + counts[2], label: "Concen X", color: "#F15628"}
    ]
  }]
});
piechart.render();
}
```


# License
```xml
Copyright 2020 READ (Bobae Kim, Dongwook Kim, Eunyoung Ha)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

