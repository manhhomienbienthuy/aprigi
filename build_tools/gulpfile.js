// Load basic plugins
var gulp = require('gulp');
var gulpif = require('gulp-if');
var argv = require('yargs').argv;
var production = !!argv.production; // --production

// Load plugins for stylesheet task
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var csslint = require('gulp-csslint');
var shorthand = require('gulp-shorthand');
var combine = require('gulp-combine-mq');
var cssmin = require('gulp-clean-css');

// Load plugins for javascript task
var eslint = require('gulp-eslint');
var babel = require('gulp-babel');
var es2015 = require('babel-preset-es2015');
var uglify = require('gulp-uglify');

gulp.task('stylesheet', () => {
    return gulp
        .src('../static_src/scss/vpyeu.scss')
        .pipe(sass())
        .pipe(autoprefixer({browsers: ['last 2 versions', '> 1%', 'iOS 7']}))
        .pipe(csslint('.csslintrc.json'))
        .pipe(csslint.reporter())
        .pipe(shorthand())
        .pipe(combine())
        .pipe(gulpif(production, cssmin()))
        .pipe(gulp.dest('../static/css/'));
});

gulp.task('javascript-root', () => {
    return gulp
        .src('../static_src/js/*.js')
        .pipe(eslint('.eslintrc.json'))
        .pipe(eslint.format())
        .pipe(babel({presets: [es2015]}))
        .pipe(gulpif(production, uglify()))
        .pipe(gulp.dest('../static/js'));
});

gulp.task('javascript-mod', () => {
    return gulp
        .src('../static_src/js/mod/*.js')
        .pipe(eslint('.eslintrc.json'))
        .pipe(eslint.format())
        .pipe(babel({presets: [es2015]}))
        .pipe(gulpif(production, uglify()))
        .pipe(gulp.dest('../static/js/mod'));
});

gulp.task('javascript-lib', () => {
    return gulp
        .src('../static_src/js/lib/*.js')
        .pipe(gulp.dest('../static/js/lib'));
});

gulp.task('javascript', [
        'javascript-root',
        'javascript-mod',
        'javascript-lib'
    ]
);

gulp.task('images', () => {
    // At this time, it simply copy all images file
    return gulp
        .src('../static_src/img/*.{jpg,jpeg,png,gif,ico,svg}')
        .pipe(gulp.dest('../static/img'));
});

gulp.task('watch', () => {
    gulp.watch('../static_src/scss/*.scss', ['stylesheet']);
    gulp.watch('../static_src/js/**/*.js', ['javascript']);
    gulp.watch('../static_src/images/*.{jpg,jpeg,png,gif,ico,svg}', ['images']);
});


gulp.task('default', ['stylesheet', 'javascript', 'images']);
