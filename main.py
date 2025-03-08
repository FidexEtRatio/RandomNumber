from nasa_source import get_current_sun_data
from entropy import get_entropy

#get_current_sun_data()
entropy = get_entropy("./images/20250308_092634_4096_0171.jpg")
print(entropy)

# test entropies:
# HMI171 = 6.5415983
# 211193171n = 6.701223
# 0094 = 6.7808456
# 0131 = 5.93037
# HMIBC = 4.6175113
# 0171 = 6.8162866