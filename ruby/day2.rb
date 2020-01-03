#!/usr/bin/ruby -w

require_relative 'library/intcode'

STDIN.readlines.each do |line|
    prog = line .sub(" ", "")
    prog = prog .split(",").map { |s| s.to_i }
    
    comp = IntCode .new(prog, 12, 2)
    puts ("Part 1: #{comp .run}")

    for noun in 0..100 do
        for verb in 0..100 do
            c = IntCode .new(prog, noun, verb)
            result = c .run
            if result == 19690720 then
                puts ("Part 2: #{100 * noun + verb}")
                exit
            end
        end
    end    
end
