#!env ruby

# frozen_string_literal: true

require "optparse"

Options = Struct.new(:modlet, :major, :minor, :patch, :verbose, :pretend) do
  def modlet_name
    modlet.to_s.split("/").last
  end
end

class Version
  attr_accessor :major, :minor, :patch

  def initialize(versions, options)
    @major, @minor, @patch = versions.split(".").map(&:to_i)
    @options = options
  end

  def version
    return [@options.major, @options.minor || 0, @options.patch || 0] if @options.major
    return [@major, @options.minor, @options.patch || 0] if @options.minor
    return [@major, @minor, @options.patch] if @options.patch

    [@major, @minor, @patch + 1]
  end

  def to_s
    version.join(".")
  end
end

options = Options.new(verbose: 0)

opt_parser = OptionParser.new do |opts|
  opts.banner = "Usage: vbump [options] <modlet>"
  opts.separator ""

  opts.on("-M", "--major VERSION", "Bump to this MAJOR") { |major| options[:major] = major }
  opts.on("-m", "--minor VERSION", "Bump to this MINOR") { |minor| options[:minor] = minor }
  opts.on("-p", "--patch VERSION", "Bump to this PATCH") { |patch| options[:patch] = patch }

  opts.separator ""
  opts.on("-v", "--[no-]verbose", "Run verbosely") { |v| options[:verbose] = v ? (options[:verbose] || 0) + 1 : 0 }

  opts.separator ""
  opts.on("--modlet MODLET", "The modlet to bump") { |modlet| options[:modlet] = modlet }
  opts.on("--pretend", "Don't actually write anything") { |pretend| options[:pretend] = pretend }
end

opt_parser.parse!
options.modlet ||= ARGV[0]

raise "Please provide a modlet to inspect" if options.modlet.nil?
raise "Invalid modlet (could not find a ModInfo.xml file for #{options.modlet_name})" unless File.exist?("#{options.modlet}/ModInfo.xml")

File.open("#{options.modlet}/ModInfo.xml", "r+") do |file|
  contents = file.read
  current_version = contents.match(/<Version value="(.+)"\s+\w/)[1]

  version = Version.new(current_version, options)

  puts "Bumping version for #{options.modlet_name} to #{version}" if options.verbose > 0
  puts "From version #{current_version}" if options.verbose > 1

  contents.gsub!(/<Version value="\d+\.\d+\.\d+/, "<Version value=\"#{version}")

  next if options.pretend

  file.rewind
  file.write(contents)
end
