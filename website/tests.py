# tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from io import BytesIO
import urllib.request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from website.models import Vehicles  # Import your Vehicles model

class VehicleUploadTest(TestCase):

    def setUp(self):
        # Create an owner user
        self.User = get_user_model()
        self.owner_username = "My_Owner"
        self.owner_password = "owner@123"
        self.owner = self.User.objects.create_user(username=self.owner_username, password=self.owner_password, is_owner=True, is_customer=False)

        # Create a client for making requests
        self.client = Client()

        # Vehicle data (list of dictionaries)
        self.vehicle_data = [
            {"vehicle_name": "Maruti Suzuki Alto 800", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRdRNepF3pd1eFwHbEXns8w4yTdGhO2K-5p8YjJwm7rzol9gg9HlA7ggyFLnQ&s", "rental_price": 1500, "description": "A compact and fuel-efficient hatchback, perfect for city driving."},
            {"vehicle_name": "Maruti Suzuki Alto K10", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDfnhhA5EZZ52WWagnidFsE6T-lmvsdEUQta99X2UB6IpZCY4EBSWFaOO3rg&s", "rental_price": 1600, "description": "A small hatchback with a peppy engine, ideal for city commutes."},
            {"vehicle_name": "Maruti Suzuki Swift", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpJ-X3-GoL2hqgwX0ah4lwXM_8VaFm4FseSPHXpTiaE_gX2v_WnX3lP_QLVg&s", "rental_price": 1800, "description": "A stylish and sporty hatchback with good performance."},
            {"vehicle_name": "Maruti Suzuki Baleno", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSE4zoYlM30mM9Km0OjIy0WvX9L-j1tI8758fsKKiqM97lGi75IT5enVLLpJQ&s", "rental_price": 2000, "description": "A premium hatchback with spacious interiors and comfortable ride."},
            {"vehicle_name": "Maruti Suzuki Wagon R", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFoCe5mxFaey4sk_sk27lgoASabOq82hUrolZGGahcRXfkqBAo6E27zPcXkA&s", "rental_price": 1700, "description": "A practical and spacious hatchback with a tall-boy design."},
            {"vehicle_name": "Maruti Suzuki Celerio", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSO7nfEX6vEbtE90x35SZfe2e4QCzRJDIPySZqD-Wui_a-ualr8cmuOI3vrrU&s", "rental_price": 1600, "description": "A compact and efficient hatchback, ideal for city commutes."},
            {"vehicle_name": "Maruti Suzuki Dzire", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdJDBqm4Ajf7EK8aTVnNHqPgW1FSlbajrkLny134JRn_Kruf9kgWw_hyHSCw&s", "rental_price": 2200, "description": "A compact sedan with a comfortable ride and good fuel efficiency."},
            {"vehicle_name": "Maruti Suzuki Ertiga", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUNZzwpnGO7Fx427wjmjP2ilL6-CsPjdpN2p-Gdc33TGhnA4XGAFlGftZNvZQ&s", "rental_price": 2800, "description": "A spacious and versatile MPV, perfect for family trips."},
            {"vehicle_name": "Maruti Suzuki Brezza", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBMziwk9jrdt5Hk8ed1uxtOO0CeQ0jmvbvZH1Vn9JdCMpW2MoYFmtRUF1lNI4&s", "rental_price": 2500, "description": "A compact SUV with a bold design and good ground clearance."},
            {"vehicle_name": "Maruti Suzuki Grand Vitara", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVpTU6xaJlJNqUYetbIO6zrKE-2zKV4N7qYa9WOpsJiNBrpIRJbqEOOiM92w&s", "rental_price": 3500, "description": "A premium SUV with a strong hybrid powertrain and spacious interiors."},
            {"vehicle_name": "Maruti Suzuki S-Presso", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHGL7v-3UKK-2IvQ-4wVJw_HsI1rbMXc4fJ5DQepLdtm4-tSOxtmP0U5yZmw&s", "rental_price": 1400, "description": "A mini-SUV styled hatchback with a peppy engine."},
            {"vehicle_name": "Maruti Suzuki Ignis", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8npOFfTr8TM0Z4umTU_njhjKcvt1qYt_7Zx5GAow8Ihfq_VjVXnmXnwszEA&s", "rental_price": 1900, "description": "A compact urban hatchback with a quirky design."},
            {"vehicle_name": "Maruti Suzuki Ciaz", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTinroarGlZCbH26sBxUEFcS2sUjd3cseQQiijDRGCzbjwOlQQvRoIQsPF8Bw&s", "rental_price": 2600, "description": "A mid-size sedan with a comfortable ride and spacious interiors."},
            {"vehicle_name": "Maruti Suzuki XL6", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrBSVn7m_oanUI08niuqiK_STnrEQ-bKE-BZCLGYxEF63GbCQQiI-8FGIItA&s", "rental_price": 3000, "description": "A premium MPV with a spacious cabin and comfortable ride."},
            {"vehicle_name": "Maruti Suzuki Eeco", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8sjA9Danm1mqMUoAt1fVJV8kSMfzXdUjOpXWJ0Ks9oJsSRiMIdKwwRYFfN6Y&s", "rental_price": 1800, "description": "A versatile van with a spacious cabin and affordable price."},
            {"vehicle_name": "Hyundai Santro", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUf59dbVzFB1YJZjXLroil_0NqRsxJg7V2WUKoF4eJfpZIkjNgxlgPuUgV1g&s", "rental_price": 1500, "description": "A compact and affordable hatchback, perfect for city driving."},
            {"vehicle_name": "Hyundai i10 Grand Nios", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbDWPREC6t3nszW4y8iy-ZoZATu2rpgwimlCfmvjMnH-oSWF0_mBFv-AqK2A&s", "rental_price": 1800, "description": "A stylish and feature-rich hatchback with a comfortable ride."},
            {"vehicle_name": "Hyundai i20", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_5fqRyjj4VUH1YNHBjbU3a5VieZOQmLWbqEdOuJgb_VFNxXu2lMQB9oza4A&s", "rental_price": 2200, "description": "A premium hatchback with a stylish design and a host of features."},
            {"vehicle_name": "Hyundai Aura", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-PO_LdJFkSUmSLL6gN3M-876DXnQ3ZiVo1SDmraaUG6DdBcak1CW7UUIGzw&s", "rental_price": 2000, "description": "A compact sedan with a stylish design and comfortable interiors."},
            {"vehicle_name": "Hyundai Verna", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-USZidX5-23aJCLOYhfXBZ5C_xdFutfCh84__b2X_8zitZsmWcu2WnGpTe_E&s", "rental_price": 2800, "description": "A mid-size sedan with a sporty design and powerful engines."},
            {"vehicle_name": "Hyundai Creta", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR14xvurzukj5LvoUMtQFrVH7xkGGn-ToVHPgSIthNWzXOiO7jmyenA50g5YA&s", "rental_price": 3200, "description": "A popular compact SUV with a stylish design and a comfortable ride."},
            {"vehicle_name": "Hyundai Venue", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRll-9ypMWsTjWgNVubHoYWhHvjypZHDtm7t865K1NvR_03P_oXuZ3v8kfLvw&s", "rental_price": 2500, "description": "A compact SUV with a stylish design and a feature-rich cabin."},
            {"vehicle_name": "Hyundai Alcazar", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdcGCwNb7_fZX61FPo3AF5f2L8f9N1Ak_DpaR1WpqnYvM2ZGUW5zdhRQjRfO8&s", "rental_price": 3800, "description": "A three-row SUV with a spacious cabin and comfortable ride."},
            {"vehicle_name": "Hyundai Tucson", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-zR5dpCn7iYfQOJ9TR7Nz82NnUReqh8R9vIHmgtkIeUq7IfzpdHXpv-7HUA&s", "rental_price": 4200, "description": "A premium SUV with a stylish design and comfortable interiors."},
            {"vehicle_name": "Hyundai Kona Electric", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIF6z00khA2ER-Y-ganR_bj0M_oJBXqNze3J6GE5l0dELktn1C6oNhElZiKA&s", "rental_price": 4000, "description": "An electric SUV with a good range and stylish design."},
            {"vehicle_name": "Tata Tiago", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQi5rKCGa_Rkb0r6vsijUg3vjDpqQTHoX-6MZ51trxqHL5Jn6CZLZubYK2PeA&s", "rental_price": 1600, "description": "A stylish and affordable hatchback with good safety features."},
            {"vehicle_name": "Tata Punch", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4DG1kQWa-FQatkhWtAewsjDJEkChHEKxm925b7QK0VaSd8d3PbRQE-V5CR4I&s", "rental_price": 1900, "description": "A sub-compact SUV with a rugged design and good ground clearance."},
            {"vehicle_name": "Tata Altroz", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjRlcGifE-iCxdhaBCqRfcJdRrvSzF7lli6dp4WBhQ7IumSdupsuE8zbwiVso&s", "rental_price": 2100, "description": "A premium hatchback with stylish design and a comfortable ride."},
            {"vehicle_name": "Tata Nexon", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFEryRc3ttN9wHuU6jL_5_wreSrJ2vb3u2JfJAOf5KVQ_Ll5-gq7xyTi2HbZE&s", "rental_price": 2600, "description": "A compact SUV with a stylish design and good safety rating."},
            {"vehicle_name": "Tata Harrier", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQcAChMVopXmo4GEJg5BvO-CiN1X1gIdbI5hk3KuslvppsJ_qhJmO9CjDre1g&s", "rental_price": 3800, "description": "A mid-size SUV with a powerful engine and spacious interiors."},
            {"vehicle_name": "Tata Safari", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsCkp4FKEFmLGy_uT6kqUbqpH77ijfNMzljl32Ig-ct9URWWsWiORqu_S7dg&s", "rental_price": 4200, "description": "A three-row SUV with a spacious cabin and comfortable ride."},
            {"vehicle_name": "Mahindra KUV100", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2QGthtP0dny9J05deag7ak5Jd8Yo-bOdsWVT-nNJkXQEeR6Zk0uFYDR4oHQ&s", "rental_price": 1700, "description": "A compact SUV with a unique design and spacious interiors."},
            {"vehicle_name": "Mahindra XUV300", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpYdRvdIYiQksxJqXysgxb6KYhcbk-ExmZB3_asvly9M4CKee8erPi1hD3Jw&s", "rental_price": 2700, "description": "A compact SUV with powerful engines and good safety features."},
            {"vehicle_name": "Mahindra Scorpio", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJx-uaSAVj3caiuP8SQufMww3g5QtFEg30Dl4i60bj8FDrCZEnnhmpGeRhtyY&s", "rental_price": 3500, "description": "A rugged SUV with a powerful engine and good off-road capabilities."},
            {"vehicle_name": "Mahindra Thar", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoxBmfWQ5Y7ksWWYaqbmpF_CL-MdFqTHW0sKeB2dXepsyw8e_WAN6vvnoU_dQ&s", "rental_price": 4000, "description": "An iconic off-road SUV with a rugged design and powerful performance."},
            {"vehicle_name": "Mahindra XUV700", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS71kNvQxrwL3GOl0vUc6reQhtQ6i09eZAg5IUeKqdAf9af7TzTHzQ9i9O7Qg&s", "rental_price": 4500, "description": "A premium SUV with advanced features, powerful engines, and spacious interiors."},
            {"vehicle_name": "Mahindra Bolero", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQSN6OM9BTWz6dOEe9ZuSE3dOR7DaLMEWK137Mmpr7hrji5wbKLdMdl5n1IaQ&s", "rental_price": 2800, "description": "A rugged and reliable SUV with a spacious cabin."},
            {"vehicle_name": "Mahindra Marazzo", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs-3dylgmUpzoeEnqooumS0G87pcWX3pI3C_SCSl_4C5pevZs1Skceahjarw&s", "rental_price": 3200, "description": "A spacious MPV for family trips."},
            {"vehicle_name": "Toyota Glanza", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTz0ZPQjHodE8yo9yJwqOLX3qTydhDIC0ifbSJv9Gy8y-47DPpHJj48Nkg-Zw&s", "rental_price": 2100, "description": "A premium hatchback with a stylish design and a comfortable ride."},
            {"vehicle_name": "Toyota Innova Crysta", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCMx83UZ8D4X3ze5rldxbAjaoFsW4XfT2A2HJ1tKwei0Qaw_2D70pziPWrcA&s", "rental_price": 4500, "description": "A spacious and comfortable MPV, perfect for family trips."},
            {"vehicle_name": "Toyota Fortuner", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVe5fXk2Nn2Jg2RcLKzZeEeorOHIo1VRDyCGo0Euw6a0Mard7HUosr4Y22KA&s", "rental_price": 5500, "description": "A powerful and rugged SUV with a spacious cabin and good off-road capabilities."},
            {"vehicle_name": "Toyota Urban Cruiser", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJoOkyAPITUzfxonvLQeATBfLzvkSrk5Qrje9MCVgCmLfSFRepRVT5u35NCw&s", "rental_price": 2700, "description": "A compact SUV with a stylish design."},
            {"vehicle_name": "Toyota Camry", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQmFJV4FCxds22BVVENXRmvHx9yKUa7RNPS9xJyFmHgT5A-dh0KvAXNzjPbA&s", "rental_price": 5000, "description": "A comfortable and luxurious sedan with a hybrid option."},
            {"vehicle_name": "Honda Amaze", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXBepVMtdctx4SR3MCl67GvfmLj2Jvz4MxIcLml3DiEP8yEpYeOqjV2RiykSg&s", "rental_price": 2300, "description": "A compact sedan with a spacious cabin and good fuel efficiency."},
            {"vehicle_name": "Honda City", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmlTy4eruWLc8QSFDHZxb96uqPGrQuiBnC2iiI0709ydlY4aele7xFC_OA1kc&s", "rental_price": 3000, "description": "A mid-size sedan with a refined engine and a comfortable ride."},
            {"vehicle_name": "Honda WR-V", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTRVg60d414KRKIkuVOxlj2fORilaBujMqdGPcdCiXtpxvf_gnxykKVPB0sOnA&s", "rental_price": 2700, "description": "A crossover with a spacious cabin and a comfortable ride."},
            {"vehicle_name": "Honda Jazz", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSispkFKqYdSU-5uDoZx6XA9dOIo1cpJmIcNVwHaBG0DWrBvSmKvkoRLknwxw&s", "rental_price": 2400, "description": "A premium hatchback with a spacious and versatile cabin."},
            {"vehicle_name": "Honda Civic", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJBldtHhdfTez2Jm7F7sZbsuUtUm04eHnIX9pBWLSDfIa7jyNUEtCJyDKgouQ&s", "rental_price": 3500, "description": "A sedan known for its sporty handling and comfortable interiors."},
            {"vehicle_name": "Renault Kwid", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9C9-hKYs100PHf5hl8f7wbmttRjj6IpiE0LsdIe0_h3p-nJ-MUINUSOqj-DA&s", "rental_price": 1400, "description": "An entry-level hatchback with a stylish design and good fuel efficiency."},
            {"vehicle_name": "Renault Triber", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWKTa-TFxMAfNUI8BJ45uD4xEGStHNrCgrMKRRVWfyrsQFSQl_aM0zVLBB4A&s", "rental_price": 2200, "description": "A versatile and affordable MPV with a spacious cabin."},
            {"vehicle_name": "Renault Kiger", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYdwohlcJen43epTMLvco5wDULsmv2b33pq35mt-F2NjnGHLxIrNg_FgubAK4&s", "rental_price": 2000, "description": "A compact SUV with a stylish design and affordable price."},
            {"vehicle_name": "Renault Duster", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuiHggyo2YH61rpZAXoT9_x2rP8x5pGJ3ysBQTB9dx6T_B9iZT9ldRj5liHoc&s", "rental_price": 2800, "description": "A compact SUV with a rugged design and good ground clearance."},
            {"vehicle_name": "Volkswagen Polo", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm1Ad3qfseBAXiRcL2MO4PjWg9QwfuuwIPISzTJG35pjvjk48BDm811zrIk70&s", "rental_price": 2300, "description": "A premium hatchback with a solid build quality and good driving dynamics."},
            {"vehicle_name": "Volkswagen Vento", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfvhKcS_Rr6R7txLdt-t6BISLR5oOBcbVkCZYZrzxRKdVczPVDdoQbxFd3Fc4&s", "rental_price": 2900, "description": "A sedan with a solid build quality and good driving dynamics."},
            {"vehicle_name": "Volkswagen Taigun", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRPpFbeCFUPSA4fhUUBo2yN6MyqYgiy5oWtC4GbJB1YsgM3i8QxWoVFZUaP&s", "rental_price": 3100, "description": "A compact SUV with a stylish design and good performance."},
            {"vehicle_name": "Skoda Rapid", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbvcZdXo_LhuUIy2SLD0KXwMHzcNhuhioX4wQQEOzNEp0mqZtEGCA046cGv6c&s", "rental_price": 3000, "description": "A sedan with a comfortable ride and a spacious cabin."},
            {"vehicle_name": "Skoda Kushaq", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPW_kwQ1DH6wX5SSvumsm2jpgk-4KeTuuziR0g9GcUjFep-ioS-JqRlyOtlA&s", "rental_price": 3500, "description": "A compact SUV with a stylish design and powerful engines."},
            {"vehicle_name": "Skoda Slavia", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG55Dd0kL5XmhAJO7KiszmCj8KBTBNbl4TGjg_k_spWBouuYmWhSM9VgcYBA&s", "rental_price": 3300, "description": "A sedan known for its build quality and comfortable ride."},
            {"vehicle_name": "MG Hector", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQURZI2EwOu2jYyBgPfZUq0QFNFYDtJbVyHwnf6_7ey-t2_id3OLjQFE8_ifgU&s", "rental_price": 4000, "description": "A mid-size SUV with a spacious cabin and a host of features."},
            {"vehicle_name": "MG Astor", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThQkGCzvNIBA8UnIcsTSZLVKEtzw-rA4Zn4OHaOZKGfISs5t3bPes5_xogVDU&s", "rental_price": 3800, "description": "A compact SUV with a stylish design and advanced features."},
            {"vehicle_name": "MG Gloster", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxJ2UrZ5AGF6SamR4rru-Y354sLMhLBC7O_k-pT4n-TcGmQlCwmp0rlrAaVA&s", "rental_price": 5200, "description": "A full-size SUV with a luxurious cabin and powerful engine."},
            {"vehicle_name": "MG ZS EV", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9IKcRoU8fTSqfYW3nPsLG6s3PTCKL_Tibwyd74qesugjJmAHTPd8Pp58cnA&s", "rental_price": 4500, "description": "An electric SUV with a good range and spacious cabin."},
            {"vehicle_name": "Kia Sonet", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5h1PAkejMCLsUH3WWdPC9LIbtb3gSKce4Y39qTRhikdRaE9kXg9RH-A9mpQ&s", "rental_price": 2500, "description": "A compact SUV with a stylish design and a feature-rich cabin."},
            {"vehicle_name": "Kia Seltos", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUGdMoMSraJRwFt0xPy6D-pi3syP2QqEXAcFeK61KwOvTzoEKuY7VxRVu9fQ&s", "rental_price": 3200, "description": "A popular compact SUV with a stylish design and a comfortable ride."},
            {"vehicle_name": "Kia Carens", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv2sPBSZ2uL_gr6Ka64ENNYJseOCqW0A1jetMI6GFL3RJj2ySEtw-Nbdm7SHo&s", "rental_price": 3500, "description": "A versatile MPV with a spacious cabin and a comfortable ride."},
            {"vehicle_name": "Jeep Compass", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQKfjp_SvRI3LowsBCdEeVoh4uCLeZwlhvMvKOGZjhrOG1oU11LHfIAv0K5rA&s", "rental_price": 4200, "description": "A compact SUV with a rugged design and good off-road capabilities."},
            {"vehicle_name": "Jeep Meridian", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSns5m6fu7VENPo2iSxCJgDpjss24dulr9coi-S_jyKtniDxshJT_8xp9nibg&s", "rental_price": 5000, "description": "A three-row SUV with a spacious cabin and a comfortable ride."},
            {"vehicle_name": "Nissan Magnite", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpFmNyY79pWOwGY1KSk6T_xlSLMuLyyOz7osZILp_syOqPoaiqJJRNaWqntuE&s", "rental_price": 2000, "description": "A compact SUV with a stylish design and affordable price."},
            {"vehicle_name": "Nissan Kicks", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE22Tt0hBkcIhJtN_OpKCabAuodjy5Qy5FdpCxvuO9tnUGgGZOb3iwfv5Nyw&s", "rental_price": 2600, "description": "A compact SUV with a bold design and a comfortable ride."},
            {"vehicle_name": "Ford EcoSport", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkNJLvA-RuBgMnrTnIG4-4evW7dQgUfCafJnqWRoiWUrdl2Wwd4cdkK0zPwaI&s", "rental_price": 2600, "description": "A compact SUV with a stylish design."},
            {"vehicle_name": "Ford Endeavour", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbpWALM2GJ6L88TLkIEJKohXnrkWpS0c57PkpgkLqtEEoT5E2N_PcY1p5pIA&s", "rental_price": 4800, "description": "A full-size SUV known for its ruggedness and comfort."},
            {"vehicle_name": "Fiat Punto", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTU_ScF_nyhZSTaJY5L2_oTKlPIhCV3B3S6WGr3vN59brkd6mggPKXogfxaGP4&s", "rental_price": 1900, "description": "A hatchback with good driving dynamics."},
            {"vehicle_name": "Fiat Linea", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMOOdFRgmzll3NusXa4IAQo60hpezESj_Fn-zHQQ01v7OIxOeFnKe8VWrDQQ&s", "rental_price": 2400, "description": "A sedan known for its solid build and comfortable ride."},
            {"vehicle_name": "Isuzu D-Max V-Cross", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOktMOmems9dHCeO5NqDiwrTXJokFszGUmauqDOWGk4u6Pl5Jn5rCEd73CdZM&s", "rental_price": 4500, "description": "A lifestyle pickup truck with a spacious cabin and good off-road capabilities."},
            {"vehicle_name": "Force Gurkha", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4IHYsBOBC_BFbnB-osAxPgus3PLjxCzjgtMkdYbCgLPkJvRD03GbMNP5pOhw&s", "rental_price": 3800, "description": "A rugged off-road SUV with a tough build and good capabilities."},
            {"vehicle_name": "Hindustan Ambassador", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSOcfBplreSQvDMufYWB3-CQPrdZh11rtEbMtg8Gore9tmWOh4S1fiTWs0Fqg&s", "rental_price": 1800, "description": "A classic Indian sedan with a comfortable ride and spacious cabin."},
            {"vehicle_name": "Premier Padmini", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAS9LhARgY9weL4tEMSUb9Hak01NuLDRlDSN4IwvtJVvTDmjyY7gUw7FMkMA&s", "rental_price": 1500, "description": "A classic Indian sedan with a simple design and comfortable ride."},
            {"vehicle_name": "Opel Astra", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZyDpLEErLsp7e5GdYcrl8dtozB67v6SiQBoBJWIEfpUcxUEm6LgD3dyG7bw&s", "rental_price": 2200, "description": "A sedan known for its comfort and reliability."},
            {"vehicle_name": "Daewoo Matiz", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRos964ffb46uNffgMahVSIRf20JPBP9WGPLRFIh4IZkhlTWN3kTcb-_c_MbQ&s", "rental_price": 1300, "description": "A compact hatchback ideal for city driving."},
            {"vehicle_name": "Chevrolet Beat", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4t3HZliDe4yF5JePR3_qvmrW8FZ4kZ85hK9vSTx9eZwdLGDqzQ7azpyuYaQ&s", "rental_price": 1600, "description": "A stylish and fuel-efficient hatchback."},
            {"vehicle_name": "Chevrolet Cruze", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQivpXIWVu_iGxKE_Gdkdjn3ENvx6L_F11Kd6UBlN2eL-gGsjhE7qM1X5WiQ&s", "rental_price": 2800, "description": "A sedan with a sporty design and comfortable ride."},
            {"vehicle_name": "San Storm", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN6T9ucEaMX_a2edt010E6wa4aarAaiOBe9ryYS8wpGyH5Nfm9z3VJn6B3vZ0&s", "rental_price": 2000, "description": "A convertible car with a fun driving experience."},
            {"vehicle_name": "Reva i", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeeTFcFvn1pXzuSYSfBPUngmgcjf85NM4ZRra_1cIdeU-ZeOH1h9ct_RmY2w&s", "rental_price": 1200, "description": "A small electric car for city commutes."},
            {"vehicle_name": "DC Avanti", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSruEonU3nRSmEbPJLPGTLbIz92I3cS1TnUOJDY9hLO0XWuOEsfPuKhihIJosc&s", "rental_price": 6000, "description": "A sports car with a unique design and powerful performance."},
            {"vehicle_name": "BMW 3 Series", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaQk_5ejMDwPJPsJpbGQE7v0jVJGGgwDeasdx0X15FLP3BF7aClRT6cBgIhi0&s", "rental_price": 7000, "description": "A luxury sedan with sporty handling and a refined interior."},
            {"vehicle_name": "Mercedes-Benz C-Class", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6Pg71pFTCL0Aodiw_2PD_ms0Y1Akl3uv_yqh2R69pDooBiD03ZlmHuK7nBA&s", "rental_price": 7500, "description": "A luxury sedan known for its comfort and sophisticated features."},
            {"vehicle_name": "Audi A4", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8raFE3VUXmYk81gjkA74lW2Dm2R-XG9HaGfZ9tHFqkkxmYpC84Va2ulvGEw&s", "rental_price": 6800, "description": "A luxury sedan with a comfortable ride and advanced technology."},
            {"vehicle_name": "Volvo XC60", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKCbNb1yDtZHu2EU1HOfmzZ0iiym-vNo1d9tCG-jZNrDQMnFUIQEHVGasmxw&s", "rental_price": 6500, "description": "A luxury SUV with a focus on safety and comfort."},
            {"vehicle_name": "Mitsubishi Pajero", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQxOxugwyrAfdWjWDPCoL_OdoSZk8DKUr5QkwplVeeY3Jg67pKwYYV79m3VCE&s", "rental_price": 4000, "description": "A rugged SUV with good off-road capabilities."},
            {"vehicle_name": "Maruti Suzuki Zen", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQQhjIgiJTM-ani7D9VdGNlDWaEeaHu1COI9TpgMQ12GDsFOphhjvLGU5_Wac&s", "rental_price": 1700, "description": "A classic hatchback known for its fuel efficiency and reliability."}
        ]

    def test_upload_vehicles(self):
        # Log in as the owner
        self.client.login(username=self.owner_username, password=self.owner_password)
        self.assertTrue(self.client.login(username=self.owner_username, password=self.owner_password)) #assertTrue if login success

        # Loop through the vehicle data and create vehicles
        for vehicle in self.vehicle_data:
            vehicle_name = vehicle['vehicle_name']
            image_url = vehicle['image_url']
            rental_price = vehicle['rental_price']
            description = vehicle['description']

            # Download the image from the URL
            try:
                image_name = slugify(image_url.split('/')[-1]) or 'vehicle_image'
                image_content = urllib.request.urlopen(image_url).read()
                image_file = ContentFile(image_content, name=image_name + '.jpg')  # Or .png, check URL
            except Exception as e:
                print(f"Error downloading image for {vehicle_name}: {e}")
                continue  # Skip to the next vehicle

            # Create the vehicle object
            new_vehicle = Vehicles.objects.create(
                owner=self.owner,
                name=vehicle_name,
                image=image_file,
                price=rental_price,
                description=description
            )

            # Assert that the vehicle was created successfully
            self.assertEqual(Vehicles.objects.filter(name=vehicle_name).count(), 1)
            print(f"Uploaded {vehicle_name}") # just to show that it's working.