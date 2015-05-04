#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq > stats/music_all_entities.txt
#zcat music.nt.gz | awk '{ print $2 }' | sort | uniq > stats/music_relations.txt

#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq -c > stats/music_entities_count.txt

#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq -c | awk '{ if ($1 >= 10) { print $2 } }' > stats/music_entities_mte10.txt
#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq -c | awk '{ if ($1 >= 5) { print $2 } }' > stats/music_entities_mte5.txt
#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq -c | awk '{ if ($1 >= 2) { print $2 } }' > stats/music_entities_mte2.txt
#zcat music.nt.gz | awk '{ print $1 "\n" $3 }' | sort | uniq -c | awk '{ if ($1 >= 1) { print $2 } }' > stats/music_entities_mte1.txt

./filter.py stats/music_entities_mte1.txt > music_mte1.nt
./filter.py stats/music_entities_mte2.txt > music_mte2.nt
./filter.py stats/music_entities_mte5.txt > music_mte5.nt
./filter.py stats/music_entities_mte10.txt > music_mte10.nt

gzip music_mte*.nt
