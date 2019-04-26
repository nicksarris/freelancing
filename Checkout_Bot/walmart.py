__author__ = 'Nick Sarris (ngs5st)'

import re
import time
import json
import requests
from bs4 import BeautifulSoup

class Walmart():

    def __init__(self, email, password, first_name, last_name,
                 address_1, address_2, city, state, zip_code, phone,
                 card_number, owner, expiration, cvv, item_url):

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.card_number = card_number
        self.owner = owner
        self.expiration = expiration
        self.cvv = cvv

        self.item_url = item_url
        self.scraper = requests.session()

    def pre_login(self):

        url_1 = 'https://quimby.mobile.walmart.com/m/j?service=AppVersion&method=getVersionRequired&p1=com.walmart.electronics'
        url_2 = 'https://api.mobile.walmart.com/mauth/v2/shippingPassEligible'

        response_1 = self.scraper.get(url_1)
        response_2 = self.scraper.get(url_2)
        print(response_1, response_2)
        return

    def login(self):

        url = 'https://api.mobile.walmart.com/v4/mauth/get-token'
        bot_detection_string = "MzI1ODM0NjI0AAAAAAAAAB2\/fHSNf724MiOJ1nzU03A1SWU8SRVHFUY1lPOwKeC" \
                               "jvpCv9t+PjeXwy2gjTjEYVdwYE\/T9SDxDTo4qOz49rB0y3iE\/OHjyMkKyZTPjf" \
                               "NqAQaz1V695J1qyp0GpRJ8TGNUGBc5PpjKX8lwuXiyFPenpZTcP524HoxVaLJWou" \
                               "S7p0FyGpy3RmHQENiWPUUQmSAHfUy0L+Dj6\/fwhWJszsZuL1zv7O5vLsAMg6xPi" \
                               "59cgLlLlqfpf7vBqfD1t86Acj5Xt+trkJwzUpTdsM\/vRGfJkn4wc41Syc0\/HV\/" \
                               "NcZku0U9MfiQeDUeL5GLD0j0eLmKDYD8lIZxZrKbw\/hp03eRZSFoq7OuLc9dQCD" \
                               "S7i+4\/EicwXYZIwTfonIbUFCsrPffYyDPgKrJSvz6ENm5Vblb9nC2HodmOJStm10" \
                               "u6zRVYY4pWE+7ZZ4XGZzERw+cjo3bofVdJsvneYvnH82dTh+C7h4FUpgMdI1Bb1Jz" \
                               "46aupnkSSEmo9Q+CEYBmCQzf97pOWwpKdIyolccwLnunSFARzVG09Hxm7c+Y8Kxus" \
                               "oE4eDlEZ4GcnqNW6wWue1XUhcRrEh7x1uU5pEQwxabesZ9QnOkFaiDbM1fIdhulk7o" \
                               "PJ2KnLvvtsJvRDKnXN0cuhWeVmMPSlBfuXCOiTnqgZSNLpH1e77nh3f0A3+w6A9j" \
                               "6odeAAGzfZ0+wv4Ly+38ei2YK8\/HuFTdTtdjXW\/b6LXRvV7lDDRNjJYgwf5xVwn" \
                               "ruN4Mun\/o9xrVuGTzh3IcdTj75RnzIS288k5qzExY+3Y0mVfX00lJRVl8Tg3s\/" \
                               "uIYdYTocF7XxFw+dLjqQINafNAyhSR0MBtqc4wqOlUQKtkPZCgOgr\/w7pWACcjtA" \
                               "ZveOVSoJeKqz6NMvf+FgQT52cWf+sDuJ1XwsSGwzXyipxIR+2W0EXw3nhLWPmh\/u" \
                               "fhfaYrgjHwu+INEXhzmldG0cK34dg5ny+NPZvcUAHYnXXt7SP3LhBSRtG6QAtqjU1" \
                               "ffxxQLrxN9pb82odhdGA775G2mJaNxzgAjd16+IuDQv9oat7mqMwyzaVSNX8A3K+M" \
                               "g05zvqVcOBCpUfA1eb817Syc1\/fIAhNbcCrhqoNQ+Ye4aEv0ZRY3GHBngut+0N6" \
                               "eVaSErRnLF2utxRYNmFF4HuPoiMjOVOWqI57IsFLCEjsNNkaU+Y33mdus9w0iQOz" \
                               "ra0BdrMCWEsESCcBJyVBF2pee7npSpuEv8uh4DXXUUggShbdb7y\/jPfu85DfL8D" \
                               "JRDFSWRppHPYUCpN4kEhUfrykVHfxVN41+lvPVoSgT\/50y\/ONTu3EEJe74veJi" \
                               "ZoaNE5IbQ2a5C6Cbz2eOzA0KZy9JucePbzwwL\/q9ivP\/0IGD9NSWtWXm3Oeffl" \
                               "pa5MF9euVWSlYMOYV5bDONZ5ac7\/vO9M5RF6xdDFsT2QkNB\/qMn2IChip+xGmL" \
                               "BHck7gd5E9QkSkyu\/DdZhwnL4Dg7eddiOwWvoqCiZj4AwpuaRRX6zxU0dXrwv7u" \
                               "SSqN8PaLOBW2IPcz3ULU6HgFkeGyTGz202SalkQcihoHHsHMCYlc\/8rnjTzReaZ" \
                               "gTCfQuvFYKB3NGOMKCKpwvlRxLw\/AuZQLiYAYq9ZMGihw+VRrx0VAXkG9RltQ6m" \
                               "DLegGNfm7E7aeLXMkHP6VszxeNKH1TA1dQcYgS6pxn7I9W0QmpY437HjALacoUUU" \
                               "mpMjqULFtWJIDEwYoYXRQOrBnZB5v90hCDRq5Iwo0d51ZohJGnJtHlQiNWwMvwPa" \
                               "7hnejgSdRmRq\/lVFCpx6Tj4sl\/fAeDWF14kUkvxKxnZxGVF9aR3mRVUfpUVLRpW" \
                               "bB3qIRoxm5chG8QdR9ldmlA69wSm2S9mOTB6OS1\/AaIt11C5qEpmkQ7XiIqiRLq" \
                               "FES0yt+urvVO5M46t6qJGSkBqTufh9qZpxMwZNywB6+68l4H0TcEyBBs+wuoQ2r8" \
                               "GXMxc4Bjha3kB8CtXmrOMBroDZawbPchOmCNMAOdAlSDmzFjvmZZkut3jHLOnuzN" \
                               "vUHjvMm7XxA7EsSBE1Rh1gew6VcAJlCMx5SZaES6RBR0VwaFLL5uu7cJV6DaeNBE" \
                               "+dcY2M8U9Lv\/DpWSRJGWJcymo38Tw1\/RaMtsiruP7czuyaFf8Hfo6oadJBtZLy" \
                               "FOgTK7zGiRMsnLVVmau\/2+RJwiN8W08VYwsJ1SURf7PWOnlq3DFaBGT9yv7uZMB7" \
                               "3CH9mHPWKfgnJa5BZ6amh76X+\/IgSzF8ENCDWtIJYPK7kTOlC83ZbbZFveaIlt" \
                               "2q8Oac4zraLiq8ar5TOd2iiJygtJcgYrQ0M9h8lsz5PDu6bgmGxw7C0rpBENMMo" \
                               "cKVfi5MTNS5X919XQLHHR2EtkVv9FQB1fAEOnajLIpDQ\/ywAU+DIPwPRSfZMRQ1G" \
                               "6F4oJjkcGOkZ9p4jDJ7Jm7zFlRxGCYLOpc3lfGHxdDK6ljyFSadozYPaRRST2NV4" \
                               "rtc9S4M20Ar4VkE2iSETXTsO17nF\/b\/n3Kk7agTEmHAz+dRfqCZPYeyrIxc\/2" \
                               "1z4bumEL6aBI\/puPHh0fpsXCW3SHWnR708Mu6JbE7bsL5XTAXM7fG\/cua6HybD" \
                               "TKKNJWF5br8+7fogn3oZsttwRC839BQvnp3qNoU0VFPXeV6FqsNVXTp4fC4AEMO3" \
                               "xKpHAi30a9Hq65End04uZC1HMpIcqeFjVVdYt+HySIf0nydeKqwPSSFv3PEboF5a" \
                               "Ql2LPSw0oVIcV+BfV1xiCP7qR0KM43cPssWEDcAFrsw9DfYwd1z7n7J3FI7qhw8G" \
                               "OxVs3h2xUYbSE0JAAH8LNRn+HKbohj77\/\/UcQDlorTGgvmoVc4Fj4czAUm9ZAU" \
                               "47\/mRMBZO65mkuqb\/gMgJhzzJlcc2ZdWEIqVb8QE1KrPvsILUz5Qrz\/qOcZIz" \
                               "jgC7SKXADVGpxyvCWl3gLw3mAzmUJhpxxLMCxu05Q3q97CMOITF\/k3wvrJ4VJT9" \
                               "1UDDI8qT+\/lj\/cW8I1pFRR1ci1YbhUG4ZAxJBol4b+7nJSs0zsm4DfhfcTG6Jf" \
                               "F+I9JYQkvI25yaBWho9lnSI\/5VN\/Kyfr6a2xrC6CVZD+iY87W5h8g0ebcaClhh" \
                               "zAByjbrMY3KtNmEKPsaaDyhImOmALGKU0u3jMOHayC\/xGbtSx4ZVw7Y00GFrNp3" \
                               "x409\/tvadYMHNYtUSQ5ilf5SRGUQ2wgndGLYzKxQG\/UtjIrtyCnde99R3Sbh0x" \
                               "le4naJdgeTOorX+++rDyc+QJxGw4Zz0XLEOCvkFUb\/YL3oZpGZ9vjbJI49gtoLj" \
                               "tGWHBVEeIgN8jTpIIX+kAgCaFA1KuqTR85xg0i7OdFuZ4Kc9i6czhLc+PbvqglAk" \
                               "BL8x3yYycM7O45HPjQr2T6nfHcYgTdcUrYpA9VJyCnNnLI9xFgJ0iDb1FTJI01VJ" \
                               "hNHhFw7oKLeK0KksrS0Oh21MIeoBURXcD0FCuFTMIfv6EGF3y\/6tNuLs+QleXZI" \
                               "Zf2Z8QpBnbIX2O6P6PiQMbio3UwGm1DuCSyIA12VeVGkL1cm+glQ1EaLrOGDQbG6" \
                               "cL\/G4e4eFSN6nKTYDGtGzPakZOK+epCIoocK+khyIXmOkxOKgVXBv0QOFdE6WXO" \
                               "D7MC3WqqYL7fbM5ztR8IQ0FTt5X7Od9e13UNxYXqxu5tsRpZF8nQbDvplEFBrTLO" \
                               "jLfWSCn7V7ZbnjYN7V1w97Y2fNzURoCc1tax8bn\/1KSrtvIp\/rC1vpLnLfyXPG" \
                               "Y0iqW4ON4iLqoe3jU1e8rBEEalH0ZyW1j\/oz1lyyCi8b6dvOnjLoTTx7v0AU7OR" \
                               "Tc7Zf+IWEnv2mfjuINKW2XFbBu6rF3xS9G5tq4TjgALNeFwOznSrmF1JYSCrTbHy" \
                               "vNCgfYj\/877UeYDRDMsto\/8rU7hOf2gISIIZ+sBRpHXq3ibrb+BM7MnBeF8pT6" \
                               "EZ9aYl2iU+JJETa39Rs\/B+3B+3oVEg5OBtv\/hCTafnCLVgY7omWoAshFhzNvU5" \
                               "trPlt4e808fWsUbrU18ufu69XLON9+KZ2GTTljNpcOZ66LyZ61tWHX4JKvSLVY+G" \
                               "NhvF9ywooShCJvMjdA6F7ztm086pANIQwNESg7Ifcn+IDOyX7advdQsiypzRlp1f" \
                               "UIQz0ELDioFYYmzwnpg1j3T0\/XL\/\/gliwnz0WwYhmOxHttHwq2HUUajsrHa67" \
                               "DWea3aW6LFBNkMbOkMIzHYmVu\/BU4dJJt1gzv6bSNKjkCsHeY\/lzRwZEybrcyA" \
                               "v8alZnfVqJhSvHulkOnY98u9ve3UxmNbSmtgWCSvOvjH4hoPW0pMO+kUMgTT+bnk5" \
                               "1ok4wdwXUzDlnI6jlla6Zq6feopkldplZlu3AEbVXl\/PxkjTt\/y8kNPzo4g25Xm" \
                               "Mb+lZBXWXEmXlIfnyTQKg\/RyhQWSiIf\/n9EQx2KcJ81Kb94Yv3XtVLFVhWEXfDX" \
                               "DCTwKvVopnYuhuOffMuuhsTWoeAkZWX4dRT58ljn+uHf8uAMcILHqJIwVD44tFpRw" \
                               "VyMCXQfTeVMz\/3memCNBd6am6KrYvbv42gJwlFWMobffX09wO84bFKs8IoTRXz3Z" \
                               "8+o9zrEZhY1Nkuyc9pKb9lPHKeHbPHWNeT0vLY18aPD3uS2XEP4aSBDaDeNgGW\/0" \
                               "Kw9KuWceJUcCht\/0KaNAhSeT98u67Dl1l6GxdhhmB9Umm0ks9rAzFL4QJML4sImg" \
                               "pNS7yqvcTnrf+sx\/7UxavAsBFXUbkqb\/j+tVeRY4SrweZSH7QmlCXbQS4dnSY2s" \
                               "lULwX2i0c3YAr48WKGsZhAQMX68KXFZfRbWJiqpap7CVoIMALkciZYGBHnIhqZ5+k" \
                               "4S5S1XbyyBP0Pf528Jja0ZaUDzhL0USdKYl6AzT9H2aX+bJpA5J4vYPD\/e4Hf6KV" \
                               "Skz6i\/sjJWv8ZpkvVr0CjJr11MJTAQ5Hy7B3onjcAH2xQqBCVgdJwFIdmt2aaJ79" \
                               "u5DEFlBezRg60qseXrqZI42yHWy6JZ92yvqIYtz4M895gAAM+kZXlpfMQl4\/wuyJ" \
                               "N4\/5Ow5SKb+xNDF2IKYpdECyeTkUSiEeu9UWMgQlLVVqQNyqm+N4hF4HmfH8zC\/" \
                               "Aa\/pVnD7R3j7C6505TpaI5EmpYByCBchQZg8HYlNvMbptXPBjCZYRsWUx6Dfa4O" \
                               "HSnZz8qkqi0b8+TqnEC5udHjCjBg3Sadf7QVE2kYjVNQLsdFtm6g0QBuJqH5tHWb" \
                               "5jBurswGJzqbqWqxO80kiOp\/R4lhSJ5lN7+j3v2DVBF1PYzvOr0cDCDZthqed0sf" \
                               "TtBvT8X7oqw1N3q5VqlonCgeUL02F6Ds2QbynMvUOed9aZEfvIKVMw1Yn46R4LiVY" \
                               "ETfo55Vbul5hEScIWTOxnmkC41gd7rS2z6Fc3yAr0JfnSvKXFk1uGAsyczltOjUlL" \
                               "aU5QImQDBi0ibL2efcKQUj6EzCmfEBLgzkaEZZs+LoRGKyG9CCrfMw6utXCtx2X3B" \
                               "qu0xim3hdNdj\/n6uaMkXEgC1AyUwSaIZx8493uqU1wOAyKIad7USXMegA81vCGTT" \
                               "pKEup557CyP\/lG7b2BV8YlImlVMQwqXF2m9LnBkgtCmiLZTDe2zg2eGOVm9apvcH" \
                               "hXg5TosWpec6sr9ZtPX\/Q3PAEvrGw\/yF5g\/7fstwHZFm8aOHNc+KZsCCqKGUL" \
                               "VBNvOGnrsk4EKnorNIGQfAdANfB00JTRtlENUJTSG6O5QvWnws5TShJoj6NXN8DS" \
                               "puITUxVMgVEvMf1sgkbmNOs81aF1lBaMM7T\/msJA65rkSOayJrkqoOICa+KSIfcy" \
                               "8FZSyVw1gKyavU+YAPR7SJW++lwE2emfyB7tzp3gZJZDxsXyjTOXp244UWrdv6xzP" \
                               "B3nS3r\/sh0tpGr7dC0TsRDbu5tu\/5MOCdAxPDo80rFKCoBtuUJi1p2x5zWu8Hz7" \
                               "+UJZaC4zyy2Ezo9N5Umvg+NN9mJndZmzZsTMoUe5+E3NQt4hi4mww2bXJwfeVi4qr" \
                               "LbRbjLtIsnmjwYlcFA3hh2V+RRMrgP\/ySkxHiIXddJyBFBlS9djK2zAGsG0Oa5mx" \
                               "mnuoavSqARnW+Psv07z7s\/ATkCEzhj\/r\/gtJn1+OBkX5lR7girCDpivn6J\/i" \
                               "jnNrISnLd4c10Aqoi83NiAybN4pLkFK+xF3NG2SPyQzyq1BESZFkDkkNwHEbUjHuC" \
                               "T+3879IRCkj6Qe2rK2BXtPL1OAy7zAPK6\/tVUdcPJ0BNeHjdPm90E9n7WftsiFUG" \
                               "kTUwCnEjci9\/4jLi86u5BE78uPsyOSLB4Z6qrpI5yP9OD2ToV6deGFe76iJ3gnsM" \
                               "18HAA4e3Yi3Y26GAy2I4hbFNT\/1zu96VYEEId0TC5TlE6yh4t31Oq5jC+oaAwrg6" \
                               "6CpFN6b7XucRCIfX2Pbm5segCJtQ2jebeNE1zXu7ZEQgkfWI0fG4rAR9MDJWB58pF" \
                               "loJjfkgFscsrJ0kdNReijzoAazQnJSb8ffr31I39Z96a4rIApfZb+zXB83VDZKlXC" \
                               "dmLMQ+eM6hEkYrRNMi9HuvF0EG6eenECqviWnlp7v5\/83lQzwpmfxra+FSGDt9oj" \
                               "nBtqKRjzA9Rkt8d4GM1OFn2jBkQfk\/NiMQ1gcDB\/R8zUGMDmoUeNyx911smE6rY9" \
                               "MJyBuGxqkzWtuqoQVldjYLHJJr0yiVZrUAufT5r5S\/T8J\/KvzGrHlURT25SmPKc" \
                               "foU9NuiJGC+af\/617jLWKq0U5TKxIwGAlC+uGrIB6mqGaQtDwftEpfL8AnnDLdvR" \
                               "bvm1Uj9fycU\/aecIL7ipi3D3DEC71Bv16+uu79JCROhZRxNYTEiIs2n0bHfg8wQug" \
                               "5oYuuCotMIL576lrqFxGsI0d1k8JhI3cDe7Mn5m+Y4ROh+BKQIOHexA0FvI9n6s9vI5" \
                               "eNKuDDD+7K+2GC2Ar6Ym\/OgDSp8At+vZyzbDA7ECzDn9dmAzS\/+zXcnBQuh42ou5Q" \
                               "WssORnngo+tTOOoWr28pUbsX6IiUTY89lkO1pWCy9sHmbHDlz9Gfnbmwvoa3UDbb8OG" \
                               "D90X3B9elwud5BVeEwXMQqts7yQ5LOtwOb2P1dkHznSqY4jsJbjt25JP3lONjFErKB" \
                               "XX7izEOW7PypVbNlKKG1NGV5qo78Xll5NeJ18sx9n5Q7TFNDZ2N1azgA20d0pz28Z" \
                               "mMn3+na+mJUxlq96wehiONbRIapTePLCNUbqgMUon9pChx6XbZQsTNetbdw6aZsK6" \
                               "bauSQXN2QFL29DYePtzgtedvMTs+4AqDUg0RA+Drvlp29sdtSLTLLw9PnZYDXxzHM" \
                               "6Af7LVc6pVPUAeX5hqMqmY4yk8Tw2aC\/tQmFhu49P8Tkh49SvXYzLrIy5YxtBVpV" \
                               "NSCOQ0CDLoMQmnbn\/nzdqS+v\/icNNw0GSS1NRApMO8v4uiL4U95L1wysMsKag8ov" \
                               "9xriI3clvyYeEzJFV5aXGC+AzzENQIBWxleHZLNsrjbxgR9XUxf+x3KbJP5lD+Gx" \
                               "XXgMuiNEtkb667HKtaFlXLH2wFRFRYEZHmK8nyBSvl\/bbqQ7G3G8VObX5CK99EkM" \
                               "JfPqk10LCtPbvDPfLOsXuYRd4+ut7PMT+o3iW2+PAkppAGG1HGX90ekOu8avzXn" \
                               "qB90d9\/gdssAP9X7Ux2838wFGT9Ils9X4hgK15QkXxI04DcZQ1UKnd2gvEHR4G" \
                               "NVWX97n1uGJjQIxp2irytfq4QujRPxyFlhCn6HEqB4NJq2MnFT7zG0JaClaQuOF" \
                               "b1eb5ZUQ8\/NTZznFe0I0cibjj5FqYBVfJNFXQav2CO+\/6lmmJ91i3qqWDyuTtc" \
                               "tommjLaYlzbxdQ4xT7Xr9OqquIUlmah2y9cHgrKB5dzKQm14t6+I1dBEDSUKclhs" \
                               "suIRXz5XMQDoSQfie1lbIrYDPMWUoQ9VW3ee3GgE4U2e5cip9x1530jGUQw\/VQ2" \
                               "zr0rt1yGpJlzY\/7dNbhupZVhWewSxIIMTcEIIp0RMNaHWumX4yQpE\/AUWZMfsHOb" \
                               "3h2fuac3y\/6ldDwhGWTDkp6+gLdDb48JTKqNf+VB0RtmQ03FQLPILJym2wNiUqOJs" \
                               "\/2ebepV4VC0wGgLP7ZB9Vh1T7EufXSi84prHrqitcRa\/IfohitkeYpruCtGLjCwz" \
                               "eRkFI0UET785heh0pnEwIsxVf6SpLtRmOStMprbzcyirc+za7coxUWqOpJR60Avpa" \
                               "bbRz3Te2fUeYOFZPqGmhFbM7EXy+8raQEKtfOL4EDOe3UJEDVWmnD9ISixVu8HOxD" \
                               "KMqdndXBekJAIyLJ61OOFkX07eGDv\/JKyKslrYBGgnwWi3K2EBVgTomOb7cSMxsN" \
                               "Y7+NX3vWKNYdYA5qPrwGnbBPX9kfc8MdzBlPRUnGfxJaCOMC1WtX1nIBX7aJ6YaHw" \
                               "JRBDiM4UEEu9zbv+FlWj5zghEcs7sdh\/sYPNzGlKWzMYNrAV+VngQhfLXfAcvd+9" \
                               "gA+SavafvdbK4otS8LNFRhWN46m8szb4VnwqD6ZiZFbZM8A53Gwy+ieT1VaQfjk7G" \
                               "O\/di\/l6V4nRw\/f\/EQHaAF7LBYJHZXwOnPyhvxsnRcsy0Aq3uOw8fmuUOM8+I" \
                               "c8ZBfkbjLucVD3VTt3iNCnjCxYAt+uKicSUYEWwtqfDCMNb1L2r9YdfELS3Y8wan" \
                               "D5I8AhmPTFyRT1KpVuhN3DXKBVxoIjeYBqIRPUtXGlWkPu9FxxgUKKOZm9TjPUuN" \
                               "juB\/4bXJ75bFFLjRXmkmnW6dvtNP6ENe2PqYc0NeQsLcFWF3Sx8RKkYnhpRYlXF" \
                               "7ZYNvJ0yJaQwyMawnv7AlUYPiLve4gwFS6kHHCGf1BffXkzR1AG5rNvCZaEL+BbT" \
                               "5GOxgGwBZga4\/dvd\/2IZVG3AG3r5eTJIuK3zEAUAoGXvMscNsSroww2ulR7EzC" \
                               "LuWJ2CayxRNMPcQ6ZR9BjMuA1as\/DoUk955cXVShx\/bK\/yHyckvVkZ41rjZK+" \
                               "X2hG0uOrlJSm7sYexrLxgE\/svJChUH6oq6ayHedqvSa1W6zgvzr45Jyt0GfOOgc" \
                               "smj0wNMDZGtFT\/HYBf22vpoe97t4EFT4J9MT8avCQQTCXwa2KgmncKnDmxTpYpA0" \
                               "qdxaQVB8ND1ElxLLP2qvzJ\/FCE0rsNEeZFoOdahY+3QbsvV3GPx7ejSN+h6Lbllw8" \
                               "BrGNHheq0SQGctu1tEz6j4\/a6YXEaZ4WAq2OrnfJFNdodTcBw4RPUVYUMLybub2" \
                               "C0wW\/mgWp1IYwcE2gBdfszTjfas5y4+GQ0l3y04UXemIqqrhd9LOa5a46lFnInY" \
                               "d6wwoL6oHroDpVi\/3VcbUz5fqUsAS1cpjlJBeD7bxkty0Z1keL5uyZGj5rxSvFEw" \
                               "Q1oWRqNV7C\/S6eXz4aYksc6+dg1x87\/52Qw+RQUChlRPaIff88D9DikkqjI1YRt" \
                               "8567ZweG9LvQwL71n9DFY2bJyasE7VQdcyPBycPqzLIrWg7fSB3qzqERs7c84\/9+" \
                               "blVxIP95iNSjFWGHYEZURw2tW9P6wRKV3mH0eXHMmMhxFgdFRAURPEGXKlZ7aXd1Q" \
                               "JV+BsKwTWB6PDBMtAeGN7ixyStrKmuiWM6YJZQYvXpBfjmkBS6M2crncHTceH8Tuc" \
                               "z3QTyfkIUZB1JSfYhs18tbeh032T2FiLCnn+9hFTzQatdQRq8d9LQNFIkFwiDvl26" \
                               "nwJheBm+DVzKwFONadEx4JsS0IZ9hv\/fkXS\/V+tLUbmbRoT5z1kPYLLw7Ap9O1" \
                               "W1wB\/34HzWWJiNlkp8drFyszXLjiTn19hmT6empMMEcE91YMxT8bS9D8oET+097" \
                               "+0106"

        payload = {
            'email': self.email,
            'cartHandling': 1,
            'botDetection': {
                'screenId': 'Sign In',
                'sensorData': bot_detection_string
            },
            'password': self.password,
        }

        response = json.loads(self.scraper.post(url, json=payload).text)
        print(response)

    def get_marker(self):

        product_id = self.item_url.split('/')[-1]
        url = 'http://www.walmart.com/product/mobile/api/{0}?location=01906'.format(product_id)
        response = str(json.loads(self.scraper.get(url).text))

        marker = re.compile("'offerId':.*, 'usItemId")
        marker = str(re.findall(marker, response)).split(':')[1]
        marker = marker.split(',')[0]
        marker = str(marker).replace("'",'')
        return marker

    def main(self):

        self.pre_login()
        self.login()
        self.get_marker()

if __name__ == '__main__':
    Walmart("", "", "", "", "", "", "", "", "", "", "", "", "", "", "").main()