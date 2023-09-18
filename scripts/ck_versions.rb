#!env ruby

modlets = []
modinfo = []

`git ls-files --modified`.split("\n").each do |line|
  next unless line.match(%r|(.*/donovan-\w+)/|) do |match|
    modlets << match[1]
    modinfo << match[1] if line =~ /ModInfo.xml/
  end
end

(modlets.uniq - modinfo.uniq).each { |modlet| system("ruby ./scripts/vbump.rb -v --modlet '#{modlet}'") }
