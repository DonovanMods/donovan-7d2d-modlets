require_relative "common"

# frozen_string_literal: true

# rubocop:disable Metrics/AbcSize
module LessGrind
  # LessGrind::Blocks
  class Blocks
    include LessGrind::Common

    def self.to_xml(file)
      new(file).to_xml
    end

    def initialize(input_file)
      @default_multiplier = LessGrind::DEFAULTS[:multiplier]
      @blocks = Nokogiri::XML(File.read(input_file))
    end

    private

    def multiplier(name)
      return @default_multiplier if name.match?(/^tree(Stump|Cactus)/)
      return @default_multiplier * 2 if name.match?(/^(terr)/)
      return @default_multiplier * 4 if name.match?(/^(ore|rock|tree|woodLogPillar)/)

      @default_multiplier
    end

    def check_resource(event, name)
      resource_name = event.at_xpath("@name")&.value
      return unless resource_name
      return if name == resource_name # Skip blocks that return themselves

      count = event.at_xpath("@count")&.value
      return unless count

      new_count = xml_value(count, name)
      return if new_count == 0 || new_count == count # skip if no change

      [resource_name, new_count]
    end

    def build
      Nokogiri::XML::Builder.new do |xml|
        xml.configs do
          xml.comment(" Harvesting/Destroying Rates ")

          @blocks.xpath("//block").each do |block|
            name = block.at_xpath("@name").value

            # Skip unwanted blocks
            next if name.match?(/^planted/) # don't want to mess with farming
            next if name.match?(/Shapes$/)
            next if name.match?(/Twitch$/)

            harvest_events = block.xpath("drop[@event='Harvest']")
            destroy_events = block.xpath("drop[@event='Destroy']")

            next unless harvest_events.any? || destroy_events.any?

            ##
            ## Harvest events
            ##
            harvest_events.each do |harvest_event|
              resource_name, count = check_resource(harvest_event, name)
              next unless resource_name

              case name
              when /cntDewCollector/ # skip these blocks on harvest
                next
              when /(cntCar|cntBus|cntFire|cntPolice)/
                prob = prob_value(harvest_event.at_xpath("@prob")&.value)
                xml.set(prob, xpath: "//block[@name='#{name}']/drop[@event='Harvest' and @name='#{resource_name}']/@prob") if prob.positive?
              when "woodLogPillar100"
                xml.comment(" Wood logs should burn longer than wood (4x) ")
                value = block.at_xpath("property[@name='FuelValue']/@value").value.to_i * 4
                xml.set(value, xpath: "//block[@name='woodLogPillar100']/property[@name='FuelValue']/@value")
              end

              xml.set(count, xpath: "//block[@name='#{name}']/drop[@event='Harvest' and @name='#{resource_name}']/@count")
            end

            ##
            ## Destroy events
            ##
            destroy_events.each do |destroy_event|
              resource_name, count = check_resource(destroy_event, name)
              next unless resource_name

              case name
              when /^(farmPlotBlockPlayer|cntDewCollector)/
                next # Skip these blocks on destroy
              when "treeStump"
                prob = prob_value(destroy_event.at_xpath("@prob")&.value)
                xml.set(prob, xpath: "//block[@name='treeStump']/drop[@event='Destroy' and @name='foodHoney']/@prob")
              end

              xml.set(count, xpath: "//block[@name='#{name}']/drop[@event='Destroy' and @name='#{resource_name}']/@count")
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
      xml.comment(" Repairing/Upgrading ")
      xml.set("resourceScrapIron", xpath: "//block[@name='ironBarsCentered']/property[@class='RepairItems']/property[@name='resourceForgedIron']/@name")
      xml.set("resourceScrapIron", xpath: "//block[@name='trapSpikesWoodDmg0']/property[@class='UpgradeBlock']/property[@name='Item']/@value")
      xml.set(40, xpath: "//block[@name='trapSpikesWoodDmg0']/property[@class='UpgradeBlock']/property[@name='ItemCount']/@value")
      xml.set(
        "resourceScrapIron",
        xpath: "//block[@name='trapSpikesScrapIronMaster']/property[@class='RepairItems']/property[@name='resourceForgedIron']/@name"
      )
      xml.set(4, xpath: "//block[@name='trapSpikesScrapIronMaster']/property[@class='RepairItems']/property[@name='resourceScrapIron']/@value")
      xml.set("resourceScrapIron", xpath: "//block[@name='trapSpikesIronDmg2']/property[@class='UpgradeBlock']/property[@name='Item']/@value")
      xml.set("resourceScrapIron", xpath: "//block[@name='trapSpikesIronDmg1']/property[@class='UpgradeBlock']/property[@name='Item']/@value")
    end
  end
end
# rubocop:enable Metrics/AbcSize
