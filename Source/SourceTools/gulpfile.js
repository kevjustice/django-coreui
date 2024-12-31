const gulp = require('gulp');
const pug = require('gulp-pug');
const htmlbeautify = require('gulp-html-beautify');

gulp.task('pug', function () {
  return gulp.src('C:\\Dropbox\\Development\\DjangoCoreUITemplate\\Source\\coreui-free-bootstrap-admin-template-main\\src\\pug\\**\\*.pug') // Source directory for Pug files
    .pipe(pug())
    .pipe(htmlbeautify({ indentSize: 4 })) // Beautify HTML with 2-space indentation
    .pipe(gulp.dest('C:\\Dropbox\\Development\\DjangoCoreUITemplate\\Source\\coreui-free-bootstrap-admin-template-main\\src\\html\\')); // Output directory for HTML files
});

gulp.task('default', gulp.series('pug'));
