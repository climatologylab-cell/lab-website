import re
from django.core.management.base import BaseCommand
from publications.models import Publication
from datetime import date

class Command(BaseCommand):
    help = 'Imports National and International conference papers from provided text data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Conference Data Import...")

        # Raw data provided by user
        national_data = """
1.	Hudha, A S& Mukherjee, M 2015, ‘Creating Elderly Friendly Neighborhoods a Framework For Assessment’, Sustainable Built Environment (SBE):proceedings of a National Conference in Department of Architecture and Planning, Indian Institute of Technology Roorkee, 10-12nd April 2015.
2.	Arora, K & Mukherjee, M 2015, ‘Insight on Lively Environment of Slum Streets: Kolkata and Mumbai’, Sustainable Built Environment (SBE): proceedings of a National Conference in Department of Architecture and Planning, Indian Institute of Technology Roorkee, 10-12nd April 2015.
3.	Bansal, N, Mukherjee, M &Gairola, A 2015, ‘Smart Cities and Disaster Resilience’, Sustainable Built Environment (SBE): proceedings of a National Conference in Department of Architecture and Planning, Indian Institute of Technology Roorkee, 10-12nd April 2015.
4.	Doreshor, K, Shankar, R & Mukherjee M 2013, ‘Inclusive Planning for the basic Services to Urban poor (BSUP) under JnNURM- case Study: Surat’, Indian Cities in Transition: proceedings of the 61st National Town and Country Planners Congress, 8-10 Feb 2013; TCPO, Ahmedabad, pp. 246-249.
5.	Biradar, S, Mukherjee, M & Shankar, S 2012, ‘Sustainability Practices and Leadership in Higher Educational Institutes of India’, Excellence in higher Education: a National Conference, 28-30 June 2012, Department of Management Studies, Indian Institute of Technology, Delhi.
6.	Bansal, N, Mukherjee, M &Gairola, A 2012, ‘Sustainable Development-Crossroads at Urban Disaster Risk Management and Climate Change’, Energy Efficient Design of Buildings: Seeking Cost Effective Solutions: proceedings of a National Conference, 6-12 February 2012, DCRUST Murthal, India.
7.	Biradar, S, Mukherjee, M & Shankar, S 2012.‘Benchmarking - as a tool for sustainable buildings’ Energy Efficient Design of Buildings: Seeking Cost Effective Solutions: proceedings of a National Conference, 6-12 February 2012, DCRUST Murthal, India.
8.	Mohan, K, Flay R. G. J, Gairola, A, Mukherjee, M &Guha T 2010,‘Erosion tests forassessing wind speed amplification in the vicinity of tall buildings’, Disaster Mitigation in Housing in India- an Agenda for Future: HDMFA2010 National Research Conference, 19-20 March 2010, IIT Roorkee.
9.	Mohan, K, Gairola, A, & Mukherjee, M  2009, ‘Strategies for mitigating the adverse effects of Pedestrian level winds in the vicinity of tall buildings’,Housing and Disaster Mitigation Efforts in India- Case-studies: HDME09 National Research Conference, 18 April 2009, IIT Roorkee.
10.	Mukherjee, M 2000, ‘Habitat and Environment’, Emerging issues of Environmental Management: a National Conference, March 2000, Department of Business Management, Calcutta University.
11.	Mukherjee, M 2000, ‘Housing, Urbanization and Environment’, Urbanization and urban Development: Past, present and future, January 2000, Centre for Urban Economic Studies, Calcutta.
"""

        international_data = """
1.	Sharma, A., & Mukherjee, M. 2024. Assessing the effect of Nature-Based Solutions on Air Quality in a Residential Area of Delhi using ENVI-met. In A. W. Barbara Widera, Marta Rudnicka-Bogusz, Jakub Onyszkiewicz (Ed.), Proceedings of 37th PLEA Conference (pp. 1371–1376). PLEA. https://plea2024.pl/?page_id=8073 
2.	Kacker, K., Mukherjee, M., & Srivastava, P. 2024. Assessment of heat stress hazard at an intra-urban level: A case of Delhi, India. In A. W. Barbara Widera, Marta Rudnicka-Bogusz, Jakub Onyszkiewicz (Ed.), Proceedings of 37th PLEA Conference (pp. 464–469). PLEA. https://plea2024.pl/?page_id=8073 
3.	S Kolay, B Sihmar, & M Mukherjee.  (2023) Ways of Seeing: An Eye-tracking Study of Natural Viewing Behaviour Towards Paintings. Conference  Proceeding of 14th AHFE International Conference on Human Factors in Communication of Design- Applied Human Factors and Ergonomics. 20-24 July, 2023. Issue 90, 2023, 96-102 AHFE
4.	Chouhan, S., Narang, A., & Mukherjee, M. (2022). Multi-Hazard Risk Assessment of Schools in Lower Himalayas: Haridwar District, Uttarakhand, India (No. EGU22-4333). Copernicus Meetings.
5.	Naorem, V., Jain, K., Mukherjee, M., & Abhishek, K. (2020). Comparing Sensors for Feature Extraction. In International Conference on Unmanned Aerial System in Geomatics (pp. 19-26). Springer, Cham.
6.	Kumar, A., Sehgal, J., Mukherjee, M., & Goswami, A. (2019). Impact Zonation and Mitigation of UHI (…. through remote sensing & development of Blue-Green Infrastructure Network). in Conference Proceedings of 5th International Conference on Countermeasures to Urban Heat Islands (IC2UHI) 2019 December 2-4, 2019, Hyderabad, India
7.	Tiwari, V., & Mukherjee, M. (2019, December). Development of Conceptual Framework for the Integrated Ground and Surface Water Management Based Master Plan for the Urban Region, Case Study: Ajmer, India. In AGU Fall Meeting Abstracts (Vol. 2019, pp. GH23B-1233).
8.	Madapala, J., Mukherjee, M., & Sen, S. (2019, December). From disaster management plans to disaster risk reduction plans: A framework on spearheading paradigm shift in India. In AGU Fall Meeting Abstracts (Vol. 2019, pp. NH11B-0771).
9.	Mukherjee, M., Madapala, J., Satheesh, A. and Mandal, A., Performance–oriented Integration of Blue-Green Infrastructure in Indian Smart City Proposals, Proceedings of 10th International Conference on Urban Climate, 6-10 August 2018 in City University, New York, USA 
10.	Mukherjee, M., Madapala, J., Khadse, A., & Singh, D. (2018, August). Performance-Oriented Integration of Blue-Green Infrastructure in Indian Smart City Proposals. In 10th International Conference on Urban Climate/14th Symposium on the Urban Environment. AMS.
11.	Rahul, A., & Mukherjee, M. (2018, August). Impact Analysis of Deep Static Bluespace on Urban Heat Island: Case of Chandigarh. In 10th International Conference on Urban Climate/14th Symposium on the Urban Environment. AMS.
12.	Mukherjee, M., Blue-Green Network and Urban Infrastructure Development, in the Thematic Event on Ecosystem-based DRR in the UN Conference AMCDRR 2018, 3-6th July, 2018 at Ulaanbaataar, Mongolia
13.	Mukherjee, M. (2017). Celebrating urban water, nature and ecological processes to mitigate urban risk. WIT Transactions on Ecology and the Environment, 216, 101-111.
14.	De, B & Mukherjee, M 2017, ‘Determining Optimal Orientation for a Residential Neighbourhood in Warm Humid Climate’, Proceedings of International Conference Sustainable Built Environment 2017 in the Department of Architecture and Planning, IIT Roorkee, 3-5 Feb, 2017, Roorkee, Uttaranchal.
15.	Arora, K & Mukherjee, M 2017, ‘Analyzing Roof zone Convective Cooling with respect to variation in Openings of Parapet’, Proceedings of International Conference Sustainable Built Environment 2017 in the Department of Architecture and Planning, IIT Roorkee, 3-5 Feb, 2017, Roorkee, Uttaranchal.
16.	De, B & Mukherjee, M 2016, ‘Impact of Canyon Design on Thermal Comfort in Warm Humid Cities: A Case of Rajarhat-Newtown, Kolkata, India’, Proceedings of 4th Annual international Conference on Countermeasures to Urban Heat Island, National University of Singapore, 30 May- 1 June 2016, Singapore. 
17.	Mukherjee, M., Roy, U. K., Biswas, A., Arora, K., De, B. and Srivastava, A. (2016) ‘Changing paradigms of Affordable Housing in Independent India’, in 3rd Residential Building Design & Construction Conference - March 2-3, 2016 at Penn State, University Park PHRC, pp. 12–28
18.	Mukherjee, M 2016, ‘Next-gen Urbanization’ in the Bi-Lateral Seminar on Kyoto University Initiative for Strengthening Collaboration between India and Japan, 14 January 2016, Kyoto, Japan.
19.	Mukherjee, M 2015, ‘Disaster Risk Reduction and Sustainability’ In 4th International Workshop on Sustainable Mountain Development, 7-9 October 2015, Itanagar, India.
20.	Pawar, A. S, Mukherjee, M,& Sahu, S 2015, ‘Assessing thermal behaviour of LULC from micro-meteorological measurements’. In the Proceedings of 3rd Annual International Conference on Advances in Architecture and Civil Engineering, pp. 562–571. doi:10.5176/2301-394X_ACE15.44
21.	De, B & Mukherjee, M. 2014, ‘Urban Physics for tomorrow’s Urban Design’, In the proceedings of 30th International PLEA Conference in CEPT University, December 2014, Ahmedabad, India.
22.	Rajendran, L P, Mukherjee, M & Chani, PS 2013, ‘Symbolic Manifestations of Socio-cultural Identity in Vernacular Architecture: A Case Study of Agraharam Housing in Triplicane; South India’, In the proceedings of International Conference on CULTHIST ’13, organized by DAKAM (Eastern Mediterranean Academic Research Center) and hosted by MSGSU (Mimar Sinan Fine Arts University), 24-25 October 2013, Istanbul, Turkey.
23.	Mukherjee, M 2013, ‘Urban India: Challenges for green Infrastructure’, in the proceedings of CESB 2013 International Conference on Sustainable Building and Refurbishment for next generations, organized by Czech Technical University in Prague in association with the CIB, 26-28 June 2013, The Netherlands.
24.	Bansal, N.,  Mukherjee, M. & Gairola, A. (2013). Urban Risk Management. in the proceedings of International Conference on Challenges in Disaster Mitigation and Management organized by Centre of Excellence in Disaster Mitigation and Management, Indian Institute of Technology Roorkee, 15-17 February 2013, Roorkee, Uttrakhand.
25.	Mukherjee, M 2012, ‘Ushering Changes in Indian Cities’, In the International Symposium "Cities under Change" organized by The Centre for Built Environment in Kolkata (Calcutta), India, 17-19 October 2012, Kolkata, India.
26.	Mohan, K, Mukherjee, M Gairola A, &Kwatra, N 2012, ‘Assessing the impact of landscape elements in mitigating adverse pedestrian level winds in the vicinity of tall buildings’, in the proceedings of International Conference on Advances in Architecture and Civil Engineering (AARCV 2012) at M S Ramaiah Institute of Technology, 21-23 June 2012, Bangalore, India.
27.	S. Nitya, Mukherjee, M 2012, ‘Tensile Fabric Roof Structures’, in the proceedings of International Conference on Advances in Architecture and Civil Engineering (AARCV 2012) at M S Ramaiah Institute of Technology, 21-23 June 2012, Bangalore, India.
28.	Bansal, N, Mukherjee, M & Gairola, A 2012, ‘Compact Development as Land Use Planning Tool for Urban Disaster Management’, in the Proceedings of REAL CORP 2012- RE-MIXING THE CITY – Towards Sustainability and Resilience?,14-16 May 2012, Tagungsband- Schwechat, Austria, pp. 132-139
29.	Mukherjee, M 2011, ‘Adaptive Planning Approach for the Caribbean Islands’ Habitat’ in the proceedings of International Conference on Responding to Climate Change in the Caribbean in London, 13 – 14 June 2011, UK.
30.	Mukherjee, M 2011, Role of plants in mitigating Adverse wind effects and improving the Air-quality in the vicinity of Tall Buildings: proceedings of US-India Conference cum workshop on Air-quality and Climate Research, 14-16 March, 2011, Hyderabad.
31.	Mukherjee, M 2010, Advocating Passive Design through Rating Mechanism: proceedings of International Housing Conference on “Sustainable Housing: Charting New Frontiers”, Housing Development Board, 26- 29 January, 2010, Singapore.
32.	Mukherjee, M 2009, Vegetative roof option for Eco-cities: proceedings of 10th APSA International Congress 2009, CEPT, 24-26 November, 2009 Ahmedabad.
33.	Mukherjee, M 2009, Climatic Resiliency for Indian Cities: proceedings of 2nd India Disaster Management Congress, NIDM, Govt of India, Vigyan Bhawan, 4-6 Nov, 2009, New Delhi.
34.	Mukherjee, M 2009, A critical evaluation of green roofs for rating systems, Urban Sustainability and Green Buildings for the 21st century: proceedings of UK-India Conference, 15 May 2009, New-Delhi.
35.	Mukherjee, M, Mohan K., & Gairola A 2009, Emerging Sustainable Green Technologies for tall buildings, Urban Sustainability and Green Buildings for the 21st century: proceedings of UK-India Conference, 15 May 2009, New-Delhi. 
36.	Mukherjee, M 2008, Housing Research Agenda: Global experience vs. National Action required in India: proceedings of XXXVI IAHS World Congress on Housing Science, 3-7 November 2008, Kolkata.
37.	Mukherjee, M, John A D & Gairola A 2008, Wind loads on overhangs in Gable-roof: proceedings of International Conference on Wind and Structures, June 2008, Korea.
38.	Mukherjee, M, Mukherjee, & Snigdha S 2007, Multi-criteria analysis of a building envelope: proceedings of Third International Ar.Tec. Conference on "The Building Envelope: A complex design" 2007, Italy.
39.	Mukherjee, M 2006, Securing Non-structural Elements: proceedings of 13th Symposium on Earthquake Engineering (13SEE), 18-20 December, 2006, Department of Earthquake Engineering, IIT Roorkee.
40.	Mukherjee, M 2006, Daylight transmission through optic fiber cables: proceedings of 4th Hawaii International Conference on Arts and Humanities, 11-14 January, 2006, Hawaii International Conferences in Honolulu, Hawaii.
41.	Mukherjee, M 2005, Design of Sustainable habitat in a flood-prone zone: proceedings of MPMD-2005, Monitoring, Prediction and Mitigation of water related disaster, 12-15th January, 2005, Disaster Prevention Research Institute, Kyoto University, Japan.
42.	Mukherjee, M 2004, Urban Safety: for the city dwellers, by the city dwellers in Asian Megacities: proceedings of New Technologies for Urban Safety of Megacities in Asia, 18-19 October, 2004, IIT Kanpur and ICUS(Tokyo, Japan), Kanpur.
43.	Mukherjee, M 2004, Water, Habitat and Sustainability: Proceedings of APHW 2004 Conference, AOGS & APHW, July 2004, Singapore.
44.	Mukherjee, M 2003, Impact analysis using information technology for new intervention in existing sustainable settlement: proceedings of ISEIS'2003 Conference, International Society for Environmental Information Sciences, September 2003, Regina, Canada.
45.	Mukherjee, M 2003, An urban Water project –in hot & arid region of Jaipur, India: proceedings of  APHW 2003  Conference, 3rd Water World Forum, Disaster Prevention Research Institutes (DPRI),March 2003, Kyoto University, Japan.
46.	Mukherjee, M 2002, Urban employment for rural women- gains & challenges: proceedings of 8th Women’s World Congress, July 2002, Makerere University, Kampala, Uganda.
47.	Mukherjee, M 2002, Women, Habitat & Environment: proceedings of 8th Women’s World Congress, July 2002, Makerere University, Kampala, Uganda. 
48.	Mukherjee, M 2002, Road connectivity, Village planning and sustainability: proceedings of  International Workshop on the Pradhan Mantri Gram Sadak Yojana (PMGSY), ORFRTD  &  IFRTD (UK),  February 2002, Bhubaneswar, India.
49.	Mukherjee, M 2002, Information Technology for Sustainable Habitat: proceedings of IT Built International Conference – 2002, January 2002, IIT Kharagpur, India.
50.	Mukherjee, M 2001, Other side of the sustainable development: proceedings of XXIX IAHS World Congress on Housing, May 2001, International Association for Housing Sciences, Ljubljana, Slovenia.
51.	Mukherjee, M 2000, Habitat, Environment and Community in Cities: proceedings of International Housing Conference 2000 (IHC 2000), May 2000, Housing Development Board, Singapore.
52.	Mukherjee, M 2000, Housing for sustainable and humane cities – Calcutta Case Study: proceedings of CITIES 2000, April 2000, University of Santo Tomas, Manila, Philippines.
53.	Mukherjee, M 2000, A model for community services in Housing Complex: proceedings of XXVIII IAHS World Congress on Housing, April 2000, International Association for Housing Sciences, Abu Dhabi, UAE.
54.	Mukherjee, M 2000, Strategic Leadership in Community Property Management: proceedings of CIB W70 Brisbane Symposium 2000, June 2000, Queensland University of Technology, Brisbane, Australia.
55.	Mukherjee, M 1999, From dawn to dusk-Transportation of Rural women to and from Calcutta metropolis: proceedings of International Forum for Rural Transport and Development, 1999, London, U.K. 
56.	Mukherjee, M 1997, Construction in India Housing Scenario: proceedings of International Constructional Management-1996,LCHS,1997, Lund, Sweden.
57.	Mukherjee, M 1996, A survey work in housing Elements: proceedings of Housing Development and Management,1996, Centre for Built Environment, Calcutta, pp. 165-171.
"""
        
        self.process_data(national_data, 'national')
        self.process_data(international_data, 'international')
        
    def process_data(self, raw_text, scope):
        lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
        
        count = 0
        for line in lines:
            # Skip empty or non-item lines
            if not line[0].isdigit():
                continue
                
            # Remove leading number (e.g., "1. ")
            content = re.sub(r'^\d+\.\s*', '', line)
            
            # Extract Year (4 digits 19xx or 20xx)
            year_match = re.search(r'(\d{4})', content)
            year = year_match.group(1) if year_match else None
            
            # Extract Title: content between single quotes ‘...’
            title_match = re.search(r'‘(.*?)’', content)
            if title_match:
                title = title_match.group(1).strip()
            # Alternative: content between quotes "..."
            elif re.search(r'"(.*?)"', content):
                title = re.search(r'"(.*?)"', content).group(1).strip()
            # Else try to split by year and take the part after
            elif year:
                parts = content.split(year)
                if len(parts) > 1:
                    # Heuristic: title is often after the year
                    potential_title = parts[1].split(',')[0].strip()
                    title = potential_title if len(potential_title) > 10 else content[:100]
                else:
                    title = content[:100] + "..."
            else:
                title = content[:100] + "..."

            # Extract Authors: everything before the year
            if year:
                authors = content.split(year)[0].strip().rstrip(',')
            else:
                authors = "Unknown"

            # Check if exists
            pub, created = Publication.objects.update_or_create(
                title=title,
                defaults={
                    'category': 'conference',
                    'scope': scope,
                    'citation': content,
                    'authors': authors,
                    'publication_date': date(int(year), 1, 1) if year else None,
                    'is_active': True
                }
            )
            
            action = "Created" if created else "Updated"
            # self.stdout.write(f"{action}: {title[:50]}...")
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f"Successfully processed {count} {scope} publications."))
