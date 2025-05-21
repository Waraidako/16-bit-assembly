
; Some comment

   ; Some comment with spaces before it

mov a, 32
mov a, b
mov a, [32]
mov a, [b]
mov a, [b + 32]
mov a, [b + c]
mov [32], 32
mov [32], a
mov [a], 32
mov [a], b
mov [a + 32], 32
mov [a + 32], b
mov [a + b], 32
mov [a + b], c
mov [32 + a], b

and c
and 3289
and [130]
and [g]
and [b + 439]
and [439 + b]
and [c + d]

shr a
shl

inc a
inc c
dec a
dec c