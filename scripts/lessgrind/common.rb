module LessGrind
  # LessGrind::Common
  module Common
    def xml_value(value, name = nil)
      return 0 if value.nil?

      value.split(",").map { |v| (v.to_i * multiplier(name)).round }.join(",")
    end

    def prob_value(value)
      return 0 if value.nil?

      [(value.to_f * LessGrind::DEFAULTS[:prob_multiplier]).round(2), 1].min
    end

    def to_xml
      build.to_xml(indent: 2, save_with: Nokogiri::XML::Node::SaveOptions::DEFAULT_XML | Nokogiri::XML::Node::SaveOptions::NO_DECLARATION)
    end
  end
end
