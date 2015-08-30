let s:save_cpo = &cpo
set cpo &vim

function! spam#spam() abort
    echo 'spam'
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo
