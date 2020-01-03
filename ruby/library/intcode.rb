class IntCode

    def initialize(mem, noun, verb)
        @mem = mem.dup
        @mem[1] = noun
        @mem[2] = verb
        @pos = 0
    end

    def run
        while true
            if @mem[@pos] == 1
                @mem[@mem[@pos+3]] = @mem[@mem[@pos+1]] + @mem[@mem[@pos+2]]
            elsif @mem[@pos] == 2
                @mem[@mem[@pos+3]] = @mem[@mem[@pos+1]] * @mem[@mem[@pos+2]]
            elsif @mem[@pos] == 99
                return @mem[0]
            end
            @pos += 4
        end
    end
end