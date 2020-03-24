rootplot rootplot_config.py test.root Top_Pt_Mphi_200_Mchi_50 Top_Pt_Mphi_195_Mchi_100 Top_Pt_Mphi_200_Mchi_150 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=200 GeV" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=200|150 GeV" --title=' '
mv test/plot.pdf test/Top_Pt_Mphi_200.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_200_Mchi_50 DM_Pt_Mphi_195_Mchi_100 DM_Pt_Mphi_200_Mchi_150 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=200 GeV" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=200|150 GeV" --title=' '
mv test/plot.pdf test/DM_Pt_Mphi_200.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_200_Mchi_50 Med_Pt_Mphi_195_Mchi_100 Med_Pt_Mphi_200_Mchi_150 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=200 GeV" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=200|150 GeV" --title=' '
mv test/plot.pdf test/Med_Pt_Mphi_200.pdf

rootplot rootplot_config.py test.root Top_Pt_Mphi_2000_Mchi_500 Top_Pt_Mphi_1995_Mchi_1000 Top_Pt_Mphi_2000_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2000 GeV" --legend-entries="M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV" --title=' '
mv test/plot.pdf test/Top_Pt_Mphi_2000.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_2000_Mchi_500 DM_Pt_Mphi_1995_Mchi_1000 DM_Pt_Mphi_2000_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2000 GeV" --legend-entries="M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV" --title=' '
mv test/plot.pdf test/DM_Pt_Mphi_2000.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_2000_Mchi_500 Med_Pt_Mphi_1995_Mchi_1000 Med_Pt_Mphi_2000_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2000 GeV" --legend-entries="M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV" --title=' '
mv test/plot.pdf test/Med_Pt_Mphi_2000.pdf

rootplot rootplot_config.py test.root Top_Pt_Mphi_3000_Mchi_1000 Top_Pt_Mphi_2995_Mchi_1500 Top_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=3000 GeV" --legend-entries="M_{#phi}|M_{#chi}=3000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV" --title=' '
mv test/plot.pdf test/Top_Pt_Mphi_3000.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_3000_Mchi_1000 DM_Pt_Mphi_2995_Mchi_1500 DM_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=3000 GeV" --legend-entries="M_{#phi}|M_{#chi}=3000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV" --title=' '
mv test/plot.pdf test/DM_Pt_Mphi_3000.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_3000_Mchi_1000 Med_Pt_Mphi_2995_Mchi_1500 Med_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=3000 GeV" --legend-entries="M_{#phi}|M_{#chi}=3000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV" --title=' '
mv test/plot.pdf test/Med_Pt_Mphi_3000.pdf

rootplot rootplot_config.py test.root Top_Pt_Mphi_200_Mchi_50 Top_Pt_Mphi_2000_Mchi_500 Top_Pt_Mphi_3000_Mchi_1000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}>2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=3000|1000 GeV"
mv test/plot.pdf test/Top_Pt_Mphi_larger_2_Mchi.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_200_Mchi_50 DM_Pt_Mphi_2000_Mchi_500 DM_Pt_Mphi_3000_Mchi_1000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}>2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=3000|1000 GeV"
mv test/plot.pdf test/DM_Pt_Mphi_larger_2_Mchi.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_200_Mchi_50 Med_Pt_Mphi_2000_Mchi_500 Med_Pt_Mphi_3000_Mchi_1000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}>2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|50 GeV,M_{#phi}|M_{#chi}=2000|500 GeV,M_{#phi}|M_{#chi}=3000|1000 GeV"
mv test/plot.pdf test/Med_Pt_Mphi_larger_2_Mchi.pdf

rootplot rootplot_config.py test.root Top_Pt_Mphi_195_Mchi_100 Top_Pt_Mphi_1995_Mchi_1000 Top_Pt_Mphi_2995_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV"
mv test/plot.pdf test/Top_Pt_Mphi_equal_2_Mchi.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_195_Mchi_100 DM_Pt_Mphi_1995_Mchi_1000 DM_Pt_Mphi_2995_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV"
mv test/plot.pdf test/DM_Pt_Mphi_equal_2_Mchi.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_195_Mchi_100 Med_Pt_Mphi_1995_Mchi_1000 Med_Pt_Mphi_2995_Mchi_1500 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}=2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|100 GeV,M_{#phi}|M_{#chi}=2000|1000 GeV,M_{#phi}|M_{#chi}=3000|1500 GeV"
mv test/plot.pdf test/Med_Pt_Mphi_equal_2_Mchi.pdf

rootplot rootplot_config.py test.root Top_Pt_Mphi_200_Mchi_150 Top_Pt_Mphi_2000_Mchi_1500 Top_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}<2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|150 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV"
mv test/plot.pdf test/Top_Pt_Mphi_smaller_2_Mchi.pdf
rootplot rootplot_config.py test.root DM_Pt_Mphi_200_Mchi_150 DM_Pt_Mphi_2000_Mchi_1500 DM_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}<2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|150 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV"
mv test/plot.pdf test/DM_Pt_Mphi_smaller_2_Mchi.pdf
rootplot rootplot_config.py test.root Med_Pt_Mphi_200_Mchi_150 Med_Pt_Mphi_2000_Mchi_1500 Med_Pt_Mphi_3000_Mchi_2000 --size=1024x768 --ylabel="events" --legend-location='upper right' --gridx --gridy -e pdf --output="test" --noclean --title="M_{#phi}<2#upoint M_{#chi}" --legend-entries="M_{#phi}|M_{#chi}=200|150 GeV,M_{#phi}|M_{#chi}=2000|1500 GeV,M_{#phi}|M_{#chi}=3000|2000 GeV"
mv test/plot.pdf test/Med_Pt_Mphi_smaller_2_Mchi.pdf