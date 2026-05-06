import flet as ft


def build_combat_view(page, controller):

    def refresh():
        page.views[-1] = build_combat_view(page, controller)
        page.update()

    def on_attack_click(e):
        perso = controller.current()
        type_perso = perso.stats_ajouter

        actions = controller.dict_abilite[type_perso]["ACTION_ATTAQUE"]

        controller.available_actions = list(actions.keys())
        refresh()

    def on_action_select(action_name):
        controller.action = action_name
        refresh()

    def on_enemy_click(index):
        if controller.action is None:
            return

        cible = controller.combat.placement_ennemi[index]
        controller.do_action(cible)
        refresh()

    # ---------------- HERO UI ----------------
    hero_columns = []

    for i, hero in enumerate(controller.combat.placement_hero):
        actif = controller.current() == hero

        hero_columns.append(
            ft.Column(
                expand=1,
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.GREEN if actif else ft.Colors.BLACK,
                        content=ft.Text(hero.nom)
                    ),
                    ft.Text(f"{hero.stats['point_vie']}/{hero.stats['point_vie_max']}")
                ]
            )
        )

    # ---------------- ENNEMI UI ----------------
    enemy_columns = []

    for i, ennemi in enumerate(controller.combat.placement_ennemi):
        enemy_columns.append(
            ft.Column(
                expand=1,
                controls=[
                    ft.ElevatedButton(
                        "Cibler",
                        on_click=lambda e, i=i: on_enemy_click(i)
                    ),
                    ft.Text(ennemi.stats_ajouter),
                    ft.Text(f"{ennemi.stats['point_vie']}/{ennemi.stats['point_vie_max']}")
                ]
            )
        )

    # ---------------- ACTIONS ----------------
    action_buttons = []

    if hasattr(controller, "available_actions"):
        for a in controller.available_actions:
            action_buttons.append(
                ft.ElevatedButton(a, on_click=lambda e, a=a: on_action_select(a))
            )

    return ft.View(
        "/combat",
        controls=[
            ft.Row(hero_columns),
            ft.Row(enemy_columns),
            ft.Row([
                ft.ElevatedButton("Attaque", on_click=on_attack_click)
            ]),
            ft.Row(action_buttons),
            ft.Text(f"Tour: {controller.tour}")
        ]
    )