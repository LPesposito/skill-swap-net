from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Popula o banco com dados de demonstração (users, profiles, skills, requests, reviews, chat)"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create users
        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password"},
            {"username": "bob", "email": "bob@example.com", "password": "password"},
            {"username": "carol", "email": "carol@example.com", "password": "password"},
        ]

        created_users = {}
        for udata in users_data:
            user, created = User.objects.get_or_create(username=udata["username"], defaults={"email": udata["email"]})
            if created:
                user.set_password(udata["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user {user.username}"))
            else:
                self.stdout.write(f"User {user.username} already exists")
            created_users[user.username] = user

        # Create profiles and skills
        from users.models import UserProfile, UserSkill
        profiles = {}

        profile_data = {
            "alice": {"bio": "Dev Python e mentor", "location": "São Paulo"},
            "bob": {"bio": "Jardinagem e manutenção", "location": "Porto Alegre"},
            "carol": {"bio": "Designer gráfico freelancer", "location": "Rio de Janeiro"},
        }

        for uname, pdata in profile_data.items():
            user = created_users[uname]
            profile, pcreated = UserProfile.objects.get_or_create(user=user, defaults={"bio": pdata["bio"], "location": pdata["location"]})
            if pcreated:
                self.stdout.write(self.style.SUCCESS(f"Created profile for {uname}"))
            profiles[uname] = profile

        # Skills (offers)
        skills_map = {
            "alice": [("Python", "Ensino programação Python para iniciantes")],
            "bob": [("Jardinagem", "Manutenção de jardins e hortas")],
            "carol": [("Design", "Design de logos e materiais visuais")],
        }

        skills = {}
        for uname, skills_list in skills_map.items():
            user = created_users[uname]
            skills[uname] = []
            for name, desc in skills_list:
                s, screated = UserSkill.objects.get_or_create(user=user, name=name, defaults={"description": desc})
                skills[uname].append(s)
                if screated:
                    self.stdout.write(self.style.SUCCESS(f"Created skill {name} for {uname}"))

        # ServiceRequest and Review
        from services.models import ServiceRequest, Review

        # bob requests Python from alice
        alice = created_users["alice"]
        bob = created_users["bob"]
        carol = created_users["carol"]

        alice_python_skill = skills["alice"][0]

        sr1, sr1_created = ServiceRequest.objects.get_or_create(
            requester=bob, provider=alice, offered_skill=alice_python_skill,
            defaults={"description": "Quero aprender o básico de Python", "status": ServiceRequest.Status.COMPLETED}
        )
        if sr1_created:
            self.stdout.write(self.style.SUCCESS(f"Created ServiceRequest {sr1.id} bob->alice"))

        # Create a review for sr1
        rev1, rev1_created = Review.objects.get_or_create(
            transaction=sr1,
            defaults={"reviewer": bob, "reviewed_user": alice, "rating": 5, "comment": "Ótima aula!"},
        )
        if rev1_created:
            self.stdout.write(self.style.SUCCESS(f"Created Review for ServiceRequest {sr1.id}"))

        # alice requests Design from carol (pending)
        carol_design_skill = skills["carol"][0]
        sr2, sr2_created = ServiceRequest.objects.get_or_create(
            requester=alice, provider=carol, offered_skill=carol_design_skill,
            defaults={"description": "Preciso de um logo simples", "status": ServiceRequest.Status.PENDING}
        )
        if sr2_created:
            self.stdout.write(self.style.SUCCESS(f"Created ServiceRequest {sr2.id} alice->carol"))

        # Chat room and messages
        from communication.models import ChatRoom, ChatMessage

        room, room_created = ChatRoom.objects.get_or_create(name="alice-bob-room")
        room.participants.add(alice, bob)
        if room_created:
            self.stdout.write(self.style.SUCCESS(f"Created ChatRoom {room.name}"))
        # create messages
        m1, m1_created = ChatMessage.objects.get_or_create(room=room, sender=alice, content="Oi Bob, podemos marcar a aula?" )
        m2, m2_created = ChatMessage.objects.get_or_create(room=room, sender=bob, content="Claro, quando você prefere?" )
        if m1_created or m2_created:
            self.stdout.write(self.style.SUCCESS(f"Created sample chat messages in {room.name}"))

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
