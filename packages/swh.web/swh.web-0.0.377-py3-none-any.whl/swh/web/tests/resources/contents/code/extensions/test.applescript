repeat 5 times
    if foo is greater than bar then
        display dialog "Hello there"
    else
        beep
    end if
end repeat

(* comment (*nested comment*) *)
on do_something(s, y)
    return {s + pi, y mod 4}
end do_something

do shell script "/bin/echo 'hello'"