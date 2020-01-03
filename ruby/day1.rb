#!/usr/bin/ruby -w

class FuelCalculator

    attr_accessor :sum
    attr_accessor :sum_recursive

    def initialize
        @sum = 0
        @sum_recursive = 0
    end

    def fuel(mass)
        return [(mass / 3) - 2, 0].max
    end

    def addModule(mass)
        @sum += self .fuel(mass)
    end

    def addModuleRecursive(mass)
        _fuel = self .fuel(mass)
        _total_fuel = _fuel

        # Continue adding fuel for the fuel...
        while _fuel > 0 do
            _fuel = self .fuel(_fuel)
            _total_fuel += _fuel
        end

        @sum_recursive += _total_fuel
    end

end

########################
# Here execution starts
########################

calc = FuelCalculator .new

STDIN.readlines.each do |line|
    calc.addModule(line.to_i)
    calc.addModuleRecursive(line.to_i)
end

puts "Part 1: total fuel used is #{calc.sum}"
puts "Part 2: total fuel used is #{calc.sum_recursive}"