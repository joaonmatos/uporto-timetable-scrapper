const express = require('express');
const bodyParser = require('body-parser');

const models = require('./models');

const port = process.env.PORT || 8080;
const app = express();

const router = express.Router();

app.use(bodyParser.json());

router.get('/classes', (req, res) => {
  models.class.findAll().then((classes) => {
    res.send(classes);
  });
});

router.get('/courses', (req, res) => {
  models.course.findAll().then((courses) => {
    res.send(courses);
  });
});

router.get('/course-units', (req, res) => {
  models.courseUnit.findAll().then((courseUnits) => {
    res.send(courseUnits); 
  });
});

router.get('/faculties', (req, res) => {
  models.faculty.findAll().then((faculties) => {
    res.send(faculties);
  });
});

router.get('/schedules', (req, res) => {
  models.schedule.findAll().then((schedules) => {
    res.send(schedules);
  });
});

app.use('/', router);
app.listen(port);