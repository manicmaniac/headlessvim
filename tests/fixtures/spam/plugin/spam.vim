if exists('g:loaded_spam')
    finish
endif
let g:loaded_spam = 1

let s:save_cpo = &cpo
set cpo &vim

command! -bar -nargs=0 Spam call spam#spam()

let &cpo = s:save_cpo
unlet s:save_cpo
