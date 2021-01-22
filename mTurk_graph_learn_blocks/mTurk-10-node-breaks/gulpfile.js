const gulp = require('gulp');

const sourcemaps = require('gulp-sourcemaps');
const uglify = require('gulp-uglify');
const babel = require('gulp-babel');
const rename = require('gulp-rename');
const concat = require('gulp-concat');

gulp.task('jspsych', () => {
  return gulp.src(['./experiment/static/js/src/jspsych/jspsych/**/*.js',
    './experiment/static/js/src/jspsych/experiments/*js'])
    .pipe(sourcemaps.init())
    .pipe(concat('jspsych-combined.js'))
    .pipe(babel({
      presets: ['@babel/preset-env'],
    }))
    .pipe(uglify())
    .pipe(rename((path) => {
      path.extname = '.min.js';
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('experiment/static/js/dist'));
});

gulp.task('task', () => {
  return gulp.src('./experiment/static/js/src/task.js')
    .pipe(sourcemaps.init())
    .pipe(babel({
      presets: ['@babel/preset-env'],
    }))
    .pipe(uglify())
    .pipe(rename((path) => {
      path.extname = '.min.js';
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('experiment/static/js/dist'));
});

gulp.task('watch', () => {
  gulp.watch('experiment/static/js/src/task.js', gulp.series('task'));
  gulp.watch('experiment/static/js/src/jspsych/**/*.js', gulp.series('jspsych'));
});

gulp.task('default', gulp.series('task', 'jspsych'));
