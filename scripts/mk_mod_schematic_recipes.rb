#!env ruby

# frozen_string_literal: true

require "nokogiri"

config_dir = "/mnt/s/Games/Steam/steamapps/common/7 Days To Die/Data/Config"
items_file = "#{config_dir}/items.xml"

raise "#{config_dir} Does not exist" unless File.exist?(config_dir) && File.directory?(config_dir)

items = Nokogiri::XML(File.read(items_file))

output = Nokogiri::XML::Builder.new do |xml|
  xml.configs do
    xml.append(xpath: "/recipes") do
      items.xpath("//item").each do |item|
        schematic_name = item.at_xpath("@name").to_s

        next unless schematic_name.match(/mod.*Schematic/)
        next unless item.at_xpath("property[@name='CreativeMode']/@value").to_s == "Player"

        xml.recipe(name: schematic_name, count: 1, craft_area: "workbench", tags: "workbenchCrafting") do
          xml.ingredient(name: item.at_xpath("property[@name='Unlocks']/@value").to_s, count: 1)
          xml.ingredient(name: "resourcePaper", count: 50)
          xml.ingredient(name: "resourceGlue", count: 5)
          xml.ingredient(name: "resourceLeather", count: 2)
        end
      end
    end
  end
end

puts output.to_xml indent: 2, save_with: Nokogiri::XML::Node::SaveOptions::DEFAULT_XML | Nokogiri::XML::Node::SaveOptions::NO_DECLARATION
