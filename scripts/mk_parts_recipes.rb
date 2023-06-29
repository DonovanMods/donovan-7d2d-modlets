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
        recipe_name = item.at_xpath("@name").to_s

        next unless recipe_name.match?(/(?:armor|gun|melee).*Parts$/)

        metal = recipe_name.match?(/T[1-2].*Parts$/) ? "resourceForgedIron" : "resourceForgedSteel"
        parts = recipe_name.match?(/(Robotics|StunBaton)Parts$/) ? "resourceElectricParts" : "resourceMechanicalParts"

        xml.recipe(name: recipe_name, count: 1, craft_area: "workbench", tags: "workbenchCrafting") do
          xml.ingredient(name: metal, count: 1)
          xml.ingredient(name: "resourceDuctTape", count: 5)
          xml.ingredient(name: parts, count: 10)
        end
      end
    end
  end
end

puts output.to_xml indent: 2, save_with: Nokogiri::XML::Node::SaveOptions::DEFAULT_XML | Nokogiri::XML::Node::SaveOptions::NO_DECLARATION
