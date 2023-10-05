#!env ruby

# frozen_string_literal: true

require "nokogiri"
require_relative "lessgrind/blocks"
require_relative "lessgrind/entityclasses"

# LessGrind
module LessGrind
  DEFAULTS = { multiplier: 2.5, prob_multiplier: 1.5 }.freeze

  @config_dir = "/mnt/s/Games/Steam/steamapps/common/7 Days To Die/Data/Config"
  @mod_dir = "modlets/a-la-carte/donovan-lessgrind/Config"

  @game_files = {
    blocks_file: "#{@config_dir}/blocks.xml",
    entity_classes_file: "#{@config_dir}/entityclasses.xml"
  }

  @mod_files = {
    blocks_file: "#{@mod_dir}/blocks.xml",
    entity_classes_file: "#{@mod_dir}/entityclasses.xml"
  }

  raise "#{@config_dir} Does not exist" unless Dir.exist?(@config_dir)
  raise "#{@mod_dir} Does not exist" unless Dir.exist?(@mod_dir)

  @mod_files.each_key do |key|
    puts "Writing #{@mod_files[key]}"

    klass = key.to_s.split("_")[0..-2].map(&:capitalize).join
    File.write(@mod_files[key], LessGrind.const_get(klass).send(:to_xml, @game_files[key]))
  end
end
