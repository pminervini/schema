../tools/rdf_splitter.py --kb=music_mte5.nt.gz --train=music_mte5_train.nt --valid=music_mte5_valid.nt --test=music_mte5_test.nt --blocksize=5000

cat music_mte5_train.nt | grep "[a-zA-Z]" > tmp.txt ; mv tmp.txt music_mte5_train.nt
cat music_mte5_valid.nt | grep "[a-zA-Z]" > tmp.txt ; mv tmp.txt music_mte5_valid.nt
cat music_mte5_test.nt | grep "[a-zA-Z]" > tmp.txt ; mv tmp.txt music_mte5_test.nt
