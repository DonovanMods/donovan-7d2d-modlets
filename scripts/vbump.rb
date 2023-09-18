#!env ruby

# frozen_string_literal: true

raise "Please provide a modlet to inspect" if ARGV[0].nil?
raise "Invalid modlet (could not find a ModInfo.xml file)" unless File.exist?("#{ARGV[0]}/ModInfo.xml")

modlet = ARGV[0].split("/").last

puts "Bumping version for #{modlet}"

File.open("#{ARGV[0]}/ModInfo.xml", "r+") do |file|
  contents = file.read
  vmajor, vminor, vpatch = contents.match(/<Version value="(\d+)\.(\d+)\.(\d+)/)[1..3].map(&:to_i)

  vpatch += 1

  contents.gsub!(/<Version value="\d+\.\d+\.\d+/, "<Version value=\"#{vmajor}.#{vminor}.#{vpatch}")
  file.rewind
  file.write(contents)
end
