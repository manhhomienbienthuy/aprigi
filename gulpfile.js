'use strict';

// Load basic plugins
const gulp        = require('gulp'),
      gulpif      = require('gulp-if'),
      argv        = require('yargs').argv,
      production  = !!argv.production; // --production

// Load plugins for stylesheet task
const sass          = require('gulp-sass'),
      autoprefixer  = require('gulp-autoprefixer'),
      csslint       = require('gulp-csslint'),
      shorthand     = require('gulp-shorthand'),
      combine       = require('gulp-combine-mq'),
      cssmin        = require('gulp-clean-css'),
      sourcemaps    = require('gulp-sourcemaps'),
      plumber       = require('gulp-plumber');

// Load plugins for javascript task
const eslint  = require('gulp-eslint'),
      babel   = require('gulp-babel'),
      uglify  = require('gulp-uglify');

// Load plugins for React
const browserify = require('browserify'),
      babelify   = require('babelify'),
      source     = require('vinyl-source-stream'),
      buffer     = require('vinyl-buffer'),
      glob       = require('glob'),
      transform  = require('vinyl-transform');

const config = {
    src: {
        base: 'static_src/',
        init: function() {
            this.js         = this.base + 'js/**/*.js';
            this.js_copy    = this.base + 'js/lib/*.js';
            this.js_compile = [this.js, '!' + this.js_copy];
            this.css        = this.base + 'scss/*.scss';
            this.css_main   = this.base + 'scss/vpyeu.scss';
            this.img        = this.base + 'img/*.{jpg,jpeg,png,gif,ico,svg}';
            this.react      = this.base + 'flux/**/*.jsx';
            return this;
        }
    }.init(),
    dest: {
        base: 'static/',
        init: function() {
            this.js       = this.base + 'js';
            this.js_copy  = this.base + 'js/lib';
            this.css      = this.base + 'css';
            this.img      = this.base + 'img';
            this.react    = this.base + 'js'
            return this;
        }
    }.init(),
    autoprefixer: {
        browsers: [
            'last 2 versions',
            '> 1%',
            'iOS 7'
        ]
    },
    babel: {
        presets: [
            'es2015',
            'react'
        ]
    },
    uglify: {
        preserveComments: (node, comment) => {
            const regex = /^\/*!/mi;
            return comment.line === 1 || regex.test(comment.value)
        },
        compress: {
            unused: true,
            dead_code: true
        }
    },
    plumber: {
        errorHandler: function(error) {
            console.log(error.toString());
            this.emit('end');
        }
    }
};
config.browserify = {
    debug: true,
    entries: glob.sync(config.src.react),
    extensions: [
        ".jsx"
    ]
};

gulp.task('set-env', () => {
    const env = production ? 'production' : 'development';
    return process.env.NODE_ENV = env;
});

gulp.task('stylesheet', () => {
    return gulp
        .src(config.src.css_main)
        .pipe(plumber(config.plumber))
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(sass())
        .pipe(autoprefixer(config.autoprefixer))
        .pipe(csslint('.csslintrc.json'))
        .pipe(csslint.reporter())
        .pipe(gulpif(production, shorthand()))
        .pipe(gulpif(production, combine()))
        .pipe(gulpif(production, cssmin()))
        .pipe(gulpif(!production, sourcemaps.write('.')))
        .pipe(gulp.dest(config.dest.css));
});

gulp.task('react-lint', () => {
    return gulp
        .src(config.src.react)
        .pipe(eslint('.eslintrc.json'))
        .pipe(eslint.format());
});

gulp.task('javascript-react', ['react-lint'], () => {
    return browserify(config.browserify)
        .transform(babelify.configure(config.babel))
        .bundle()
        .on('error', config.plumber.errorHandler)
        .pipe(source('aprigi.js'))
        .pipe(buffer())
        .pipe(gulpif(production, uglify(config.uglify)))
        .pipe(gulp.dest(config.dest.react))
});

gulp.task('javascript-compile', () => {
    return gulp
        .src(config.src.js_compile)
        .pipe(plumber(config.plumber))
        .pipe(eslint('.eslintrc.json'))
        .pipe(eslint.format())
        .pipe(babel(config.babel))
        .pipe(gulpif(production, uglify(config.uglify)))
        .pipe(gulp.dest(config.dest.js));
});

gulp.task('javascript-copy', () => {
    return gulp
        .src(config.src.js_copy)
        .pipe(gulp.dest(config.dest.js_copy));
});

gulp.task('javascript', [
    'javascript-react',
    'javascript-compile',
    'javascript-copy'
]);

gulp.task('images', () => {
    // At this time, it simply copy all images file
    return gulp
        .src(config.src.img)
        .pipe(gulp.dest(config.dest.img));
});

gulp.task('watch', ['stylesheet', 'javascript', 'images'], () => {
    gulp.watch(config.src.css, ['stylesheet']);
    gulp.watch(config.src.react, ['javascript-react']);
    gulp.watch(config.src.js, ['javascript']);
    gulp.watch(config.src.img, ['images']);
});


gulp.task('default', ['set-env', 'stylesheet', 'javascript', 'images']);
