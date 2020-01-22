#!/usr/bin/ruby -w

require 'ostruct'
require 'set'

class Path
    attr_reader :path

    @@lookup = { "U" => [0,-1], "R" => [1,0], "D" => [0,1], "L" => [-1,0] }

    def initialize
        @x = 0
        @y = 0
        @path = []
    end

    def execute(command)
        dir,*rest = command.chars
        steps = rest.join('').to_i

        _move(dir, steps)
    end

    def _move(dir, steps)
        (0...steps).each do
            @x += @@lookup[dir][0]
            @y += @@lookup[dir][1]
            @path << OpenStruct.new(x: @x, y: @y, dist: @x.abs + @y.abs)
        end
    end

    def steps_to(pos)
        @path.find_index(pos) + 1 # position at index 0 is reached after 1 step
    end

    def intersections(other)
        @path.to_set & other.path.to_set
    end
end

paths = []

STDIN.readlines.each do |line|
    paths << Path.new
    line.split(',').each do |command|
        paths.last.execute(command)
    end
end

# Fetch all intersections
intersections = paths[0].intersections(paths[1])

# Find the closest one (dist)
puts "Part 1: manhattan distance to closest intersection is #{intersections.sort_by(&:dist).first.dist}"

# Find the lowest number of steps in total to reach an intersection
puts "Part 2: first intersection is reached after #{intersections.map { |pos| paths[0].steps_to(pos) + paths[1].steps_to(pos) }.sort.first} steps"
