require_relative "common"

# frozen_string_literal: true

# rubocop:disable Metrics/AbcSize
module LessGrind
  # LessGrind::EntityClasses
  class EntityClasses
    include LessGrind::Common

    def self.to_xml(file)
      new(file).to_xml
    end

    def initialize(input_file)
      @default_multiplier = LessGrind::DEFAULTS[:multiplier]
      @entities = Nokogiri::XML(File.read(input_file))
    end

    private

    def multiplier(name = nil)
      @default_multiplier
    end

    def build
      Nokogiri::XML::Builder.new do |xml|
        xml.configs do
          xml.comment(" Animal Harvesting Rates ")

          @entities.xpath("//entity_class").each do |entity|
            name = entity.at_xpath("@name").value
            harvest_events = entity.xpath("drop[@event='Harvest']")

            next unless harvest_events.any?

            ##
            ## Harvest events
            ##
            event_type = "Harvest"
            harvest_events.each do |harvest_event|
              resource_name = harvest_event.at_xpath("@name").value

              next unless name.match?(/^animal/)

              count = harvest_event.at_xpath("@count").value
              new_count = xml_value(count)
              tag = harvest_event.at_xpath("@tag")&.value

              next if count == new_count # skips if no change
              next unless tag && %w[butcherHarvest allToolsHarvest].include?(tag)

              xml.set(
                new_count,
                xpath: "//entity_class[@name='#{name}']/drop[@event='#{event_type}' and @name='#{resource_name}' and @tag='#{tag}']/@count"
              )
            end
          end

          extras(xml)
        end
      end
    end

    ##
    ## Additional Entries
    ##
    def extras(xml)
      xml.comment(" Player Speeds ")
      xml.set 2.5, xpath: "//entity_class[@name='playerMale']/effect_group/passive_effect[@name='WalkSpeed']/@value"
      xml.set 1.5, xpath: "//entity_class[@name='playerMale']/effect_group/passive_effect[@name='RunSpeed']/@value"
      xml.set 1.25, xpath: "//entity_class[@name='playerMale']/effect_group/passive_effect[@name='CrouchSpeed']/@value"
      xml.set 2.0, xpath: "//entity_class[@name='playerMale']/effect_group/passive_effect[@name='WalkSpeed'][@tags='swimming']/@value"
      xml.set 1.5, xpath: "//entity_class[@name='playerMale']/effect_group/passive_effect[@name='RunSpeed'][@tags='swimming']/@value"
    end
  end
end
# rubocop:enable Metrics/AbcSize
