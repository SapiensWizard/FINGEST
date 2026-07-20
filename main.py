from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from database import Database
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
import traceback

# Configuração
Window.size = (400, 700)

# Carregar o arquivo KV
try:
    Builder.load_file('fingest.kv')
except Exception as e:
    print(f"Erro ao carregar KV: {e}")

class DashboardScreen(Screen):
    pass

class TransacoesScreen(Screen):
    pass

class PoupancasScreen(Screen):
    pass

class ConfigScreen(Screen):
    pass

# Botão personalizado com fundo colorido
class IconButton(BoxLayout):
    def __init__(self, icon_name, bg_color, on_release_func, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self.spacing = 0
        self.padding = 0
        
        # Botão com fundo colorido
        self.btn = MDIconButton(
            icon=icon_name,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Ícone branco
            md_bg_color=bg_color,  # Fundo colorido
            size_hint=(1, 1),
            on_release=on_release_func
        )
        
        self.add_widget(self.btn)

# Classe para item de transação
class TransacaoItem(BoxLayout):
    def __init__(self, app, id_trans, tipo, descricao, valor, categoria, data, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.id_trans = id_trans
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria
        self.data = data
        
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.spacing = dp(8)
        self.padding = dp(8)
        
        # Fundo do item (opcional)
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(8)])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Definir ícone e cores baseado no tipo
        if tipo == 'receita':
            icon = "arrow-up"
            icon_bg = (0.2, 0.7, 0.3, 1)  # Verde
        else:
            icon = "arrow-down"
            icon_bg = (0.8, 0.3, 0.3, 1)  # Vermelho
        
        # Container da informação
        info_box = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.6,
            spacing=dp(4)
        )
        
        # Título (descrição e valor)
        from kivymd.uix.label import MDLabel
        title_label = MDLabel(
            text=f"{descricao} - {app.format_money(valor)}",
            font_style="Subtitle1",
            size_hint_y=None,
            height=dp(30),
            color=(0, 0, 0, 1)  # Preto
        )
        
        # Subtítulo (categoria e data)
        subtitle_label = MDLabel(
            text=f"{categoria} - {data[:10] if data else ''}",
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20)
        )
        
        info_box.add_widget(title_label)
        info_box.add_widget(subtitle_label)
        
        # Container dos botões
        buttons_box = MDBoxLayout(
            size_hint_x=0.35,
            spacing=dp(12),
            pos_hint={'center_y': 0.5}
        )
        
        # Botão Editar (fundo azul, ícone branco)
        edit_btn = IconButton(
            icon_name="pencil",
            bg_color=(0.2, 0.6, 0.8, 1),  # Azul
            on_release_func=self.editar_transacao
        )
        
        # Botão Excluir (fundo vermelho, ícone branco)
        delete_btn = IconButton(
            icon_name="delete",
            bg_color=(0.8, 0.3, 0.3, 1),  # Vermelho
            on_release_func=self.excluir_transacao
        )
        
        buttons_box.add_widget(edit_btn)
        buttons_box.add_widget(delete_btn)
        
        # Ícone de tipo (fundo colorido, ícone branco)
        type_icon = IconButton(
            icon_name=icon,
            bg_color=icon_bg,
            on_release_func=lambda x: None  # Sem ação
        )
        
        self.add_widget(type_icon)
        self.add_widget(info_box)
        self.add_widget(buttons_box)
    
    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def editar_transacao(self, instance):
        """Abre diálogo para editar a transação"""
        self.app.open_edit_transacao(self.id_trans, self.tipo, self.descricao, self.valor, self.categoria)
    
    def excluir_transacao(self, instance):
        """Exclui a transação"""
        self.app.confirm_delete(self.id_trans, self)

class FingestApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.dialog = None
        self.current_dialog = None
    
    def show_message(self, title, message):
        """Mostra uma mensagem simples usando Popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, halign='center', valign='middle'))
        btn = MDRaisedButton(text="OK", size_hint_y=None, height=dp(40))
        
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.3))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Criar o gerenciador de telas
        sm = ScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(TransacoesScreen(name='transacoes'))
        sm.add_widget(PoupancasScreen(name='poupancas'))
        sm.add_widget(ConfigScreen(name='config'))
        
        return sm
    
    def on_start(self):
        # Atualizar os dados após a interface estar pronta
        Clock.schedule_once(lambda dt: self.update_dashboard(), 0.5)
        Clock.schedule_once(lambda dt: self.update_transacoes_list(), 0.5)
        Clock.schedule_once(lambda dt: self.update_poupancas_list(), 0.5)
    
    def format_money(self, valor):
        """Formata valor para Kwanza (Kz)"""
        try:
            if isinstance(valor, str):
                valor = float(valor) if valor else 0
            return f"{valor:,.2f} Kz".replace(",", " ").replace(".", ",")
        except:
            return "0,00 Kz"
    
    def update_dashboard(self):
        try:
            saldo = self.db.get_saldo()
            dashboard = self.root.get_screen('dashboard')
            if hasattr(dashboard, 'ids') and 'saldo_label' in dashboard.ids:
                dashboard.ids.saldo_label.text = self.format_money(saldo)
            
            # Atualizar lista de últimas transações
            transacoes = self.db.get_transacoes(5)
            list_widget = dashboard.ids.transacoes_list
            if list_widget:
                list_widget.clear_widgets()
                
                for trans in transacoes:
                    id_trans, tipo, categoria, valor, descricao, data = trans
                    item = TransacaoItem(self, id_trans, tipo, descricao, valor, categoria, data)
                    list_widget.add_widget(item)
        except Exception as e:
            print(f"Erro no dashboard: {e}")
            traceback.print_exc()
    
    def update_transacoes_list(self):
        try:
            transacoes = self.db.get_transacoes(100)
            list_widget = self.root.get_screen('transacoes').ids.transacoes_list_full
            if list_widget:
                list_widget.clear_widgets()
                
                if not transacoes:
                    from kivymd.uix.label import MDLabel
                    label = MDLabel(
                        text="Nenhuma transação registrada.\nToque em + para adicionar!",
                        halign="center",
                        size_hint_y=None,
                        height=dp(100)
                    )
                    list_widget.add_widget(label)
                else:
                    for trans in transacoes:
                        id_trans, tipo, categoria, valor, descricao, data = trans
                        item = TransacaoItem(self, id_trans, tipo, descricao, valor, categoria, data)
                        list_widget.add_widget(item)
        except Exception as e:
            print(f"Erro na lista: {e}")
            traceback.print_exc()
    
    def update_poupancas_list(self):
        try:
            poupancas = self.db.get_poupancas()
            list_widget = self.root.get_screen('poupancas').ids.poupancas_list
            if list_widget:
                list_widget.clear_widgets()
                
                # Calcular poupança mensal
                saldo = self.db.get_saldo()
                poupanca_mensal = max(0, saldo)
                if 'poupanca_mensal_label' in self.root.get_screen('poupancas').ids:
                    self.root.get_screen('poupancas').ids.poupanca_mensal_label.text = self.format_money(poupanca_mensal)
                
                for p in poupancas:
                    id, nome, meta, atual = p
                    progresso = (atual / meta * 100) if meta > 0 else 0
                    
                    item = TwoLineAvatarIconListItem(
                        IconLeftWidget(icon="piggy-bank"),
                        text=f"{nome} - Meta: {self.format_money(meta)}",
                        secondary_text=f"Guardado: {self.format_money(atual)} ({progresso:.0f}%)"
                    )
                    list_widget.add_widget(item)
        except Exception as e:
            print(f"Erro nas poupanças: {e}")
            traceback.print_exc()
    
    def open_edit_transacao(self, id_trans, tipo, descricao_atual, valor_atual, categoria_atual):
        """Abre diálogo para editar uma transação"""
        try:
            content = MDBoxLayout(
                orientation='vertical',
                spacing=dp(12),
                padding=dp(12),
                size_hint_y=None,
                height=dp(300)
            )
            
            # Campo de valor
            valor_input = MDTextField(
                hint_text="Valor (Kz)",
                text=str(valor_atual).replace('.', ','),
                input_filter="float",
                helper_text="Ex: 15000,50",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            # Campo de descrição
            descricao_input = MDTextField(
                hint_text="Descrição",
                text=descricao_atual,
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            # Campo de categoria
            categoria_input = MDTextField(
                hint_text="Categoria",
                text=categoria_atual,
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            content.add_widget(valor_input)
            content.add_widget(descricao_input)
            content.add_widget(categoria_input)
            
            dialog = MDDialog(
                title=f"Editar {tipo}",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: self.close_dialog(dialog)),
                    MDRaisedButton(
                        text="Salvar Alterações", 
                        md_bg_color=(0.2, 0.6, 0.8, 1),
                        on_release=lambda x: self.save_edit_transacao(
                            id_trans, tipo, categoria_input.text, valor_input.text, 
                            descricao_input.text, dialog
                        )
                    )
                ]
            )
            
            dialog.open()
            
        except Exception as e:
            print(f"Erro ao abrir edição: {e}")
            traceback.print_exc()
            self.show_message("Erro", f"Erro ao abrir edição: {e}")
    
    def save_edit_transacao(self, id_trans, tipo, categoria, valor_str, descricao, dialog):
        """Salva a edição da transação"""
        try:
            if not valor_str or not descricao:
                self.show_message("Aviso", "Preencha todos os campos!")
                return
            
            valor_str = valor_str.replace(',', '.')
            valor = float(valor_str) if valor_str else 0
            
            if valor <= 0:
                self.show_message("Aviso", "Insira um valor válido!")
                return
            
            # Atualizar no banco
            self.db.delete_transacao(id_trans)
            self.db.add_transacao(tipo, categoria, valor, descricao.strip())
            self.close_dialog(dialog)
            
            # Atualizar interfaces
            Clock.schedule_once(lambda dt: self.update_dashboard(), 0.1)
            Clock.schedule_once(lambda dt: self.update_transacoes_list(), 0.1)
            Clock.schedule_once(lambda dt: self.update_poupancas_list(), 0.1)
            
            self.show_message("Sucesso", "Transação atualizada com sucesso!")
            
        except ValueError:
            self.show_message("Erro", "Valor inválido! Use números (ex: 15000,50)")
        except Exception as e:
            print(f"Erro ao salvar edição: {e}")
            traceback.print_exc()
            self.show_message("Erro", f"Erro: {e}")
    
    def open_add_transacao(self, tipo):
        """Abre diálogo para adicionar transação"""
        try:
            content = MDBoxLayout(
                orientation='vertical',
                spacing=dp(12),
                padding=dp(12),
                size_hint_y=None,
                height=dp(320)
            )
            
            # Campo de valor
            valor_input = MDTextField(
                hint_text="Valor (Kz)",
                input_filter="float",
                helper_text="Ex: 15000,50",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            # Campo de descrição
            descricao_input = MDTextField(
                hint_text="Descrição",
                helper_text="Ex: Salário, Compras...",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            # Campo de categoria
            categoria_input = MDTextField(
                hint_text="Categoria",
                helper_text="Digite a categoria (ex: Salário, Alimentação...)",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            # Sugestões de categorias
            from kivymd.uix.label import MDLabel
            if tipo == "receita":
                sugestoes = "💡 Sugestões: Salário, Freelance, Presente, Investimento"
            else:
                sugestoes = "💡 Sugestões: Alimentação, Transporte, Moradia, Saúde, Lazer"
            
            ajuda_label = MDLabel(
                text=sugestoes,
                font_style="Caption",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=dp(30)
            )
            
            content.add_widget(valor_input)
            content.add_widget(descricao_input)
            content.add_widget(categoria_input)
            content.add_widget(ajuda_label)
            
            dialog = MDDialog(
                title=f"➕ Adicionar {tipo}",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: self.close_dialog(dialog)),
                    MDRaisedButton(
                        text="💾 Salvar", 
                        md_bg_color=(0.2, 0.7, 0.3, 1) if tipo == "receita" else (0.8, 0.3, 0.3, 1),
                        on_release=lambda x: self.save_transacao(
                            tipo, categoria_input.text, valor_input.text, 
                            descricao_input.text, dialog
                        )
                    )
                ]
            )
            
            dialog.open()
            
        except Exception as e:
            print(f"Erro ao abrir diálogo: {e}")
            traceback.print_exc()
            self.show_message("Erro", f"Erro: {e}")
    
    def save_transacao(self, tipo, categoria, valor_str, descricao, dialog):
        """Salva a transação no banco"""
        try:
            # Validações
            if not valor_str or not valor_str.strip():
                self.show_message("Aviso", "Digite o valor!")
                return
            
            if not descricao or not descricao.strip():
                self.show_message("Aviso", "Digite a descrição!")
                return
            
            if not categoria or not categoria.strip():
                self.show_message("Aviso", "Digite a categoria!")
                return
            
            # Converter valor
            valor_str = valor_str.strip().replace(',', '.')
            try:
                valor = float(valor_str)
            except ValueError:
                self.show_message("Erro", "Valor inválido! Use números (ex: 15000,50)")
                return
            
            if valor <= 0:
                self.show_message("Aviso", "Valor deve ser maior que zero!")
                return
            
            # Salvar no banco
            self.db.add_transacao(tipo, categoria.strip(), valor, descricao.strip())
            self.close_dialog(dialog)
            
            # Atualizar interfaces
            Clock.schedule_once(lambda dt: self.update_dashboard(), 0.2)
            Clock.schedule_once(lambda dt: self.update_transacoes_list(), 0.2)
            Clock.schedule_once(lambda dt: self.update_poupancas_list(), 0.2)
            
            # Mensagem de sucesso
            self.show_message("Sucesso", f"{tipo} de {self.format_money(valor)} adicionada!")
            
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            traceback.print_exc()
            self.show_message("Erro", f"Erro: {str(e)}")
    
    def close_dialog(self, dialog):
        """Fecha o diálogo com segurança"""
        try:
            if dialog and dialog.parent:
                dialog.dismiss()
        except Exception as e:
            print(f"Erro ao fechar diálogo: {e}")
    
    def open_add_poupanca(self):
        """Abre diálogo para adicionar meta de poupança"""
        try:
            content = MDBoxLayout(
                orientation='vertical',
                spacing=dp(12),
                padding=dp(12),
                size_hint_y=None,
                height=dp(200)
            )
            
            nome_input = MDTextField(
                hint_text="Nome da meta",
                helper_text="Ex: Carro, Casa, Viagem...",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            meta_input = MDTextField(
                hint_text="Valor da meta (Kz)",
                input_filter="float",
                mode="rectangle",
                size_hint_y=None,
                height=dp(60)
            )
            
            content.add_widget(nome_input)
            content.add_widget(meta_input)
            
            dialog = MDDialog(
                title="🎯 Nova Meta de Poupança",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="Cancelar", on_release=lambda x: self.close_dialog(dialog)),
                    MDRaisedButton(
                        text="Criar Meta", 
                        md_bg_color=(0.2, 0.6, 0.8, 1),
                        on_release=lambda x: self.save_poupanca(
                            nome_input.text, meta_input.text, dialog
                        )
                    )
                ]
            )
            
            dialog.open()
            
        except Exception as e:
            print(f"Erro ao abrir poupança: {e}")
            traceback.print_exc()
    
    def save_poupanca(self, nome, meta_str, dialog):
        try:
            if not nome or not nome.strip():
                self.show_message("Aviso", "Digite o nome da meta!")
                return
            
            if not meta_str or not meta_str.strip():
                self.show_message("Aviso", "Digite o valor da meta!")
                return
            
            meta_str = meta_str.strip().replace(',', '.')
            try:
                meta = float(meta_str)
            except ValueError:
                self.show_message("Erro", "Valor inválido!")
                return
            
            if meta <= 0:
                self.show_message("Aviso", "Meta precisa ser maior que zero!")
                return
            
            self.db.add_poupanca(nome.strip(), meta)
            self.close_dialog(dialog)
            self.update_poupancas_list()
            self.show_message("Sucesso", f"Meta '{nome}' criada!")
                
        except Exception as e:
            print(f"Erro ao salvar poupança: {e}")
            traceback.print_exc()
            self.show_message("Erro", f"Erro: {e}")
    
    def clear_all_transacoes(self):
        """Remove todas as transações"""
        def confirm_clear():
            try:
                transacoes = self.db.get_transacoes()
                for trans in transacoes:
                    self.db.delete_transacao(trans[0])
                
                self.close_dialog(dialog_clear)
                self.update_dashboard()
                self.update_transacoes_list()
                self.update_poupancas_list()
                
                self.show_message("Sucesso", "Todas as transações foram removidas!")
            except Exception as e:
                print(f"Erro ao limpar: {e}")
                traceback.print_exc()
        
        dialog_clear = MDDialog(
            title="⚠️ Limpar todas as transações?",
            text="Esta ação não pode ser desfeita!\nTodas as receitas e despesas serão removidas.",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.close_dialog(dialog_clear)),
                MDRaisedButton(
                    text="Sim, limpar tudo",
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: confirm_clear()
                )
            ]
        )
        dialog_clear.open()
    
    def confirm_delete(self, id_transacao, item_widget):
        """Confirma exclusão de transação"""
        dialog = MDDialog(
            title="🗑️ Confirmar exclusão",
            text="Tem certeza que deseja excluir esta transação?",
            buttons=[
                MDFlatButton(text="Cancelar", on_release=lambda x: self.close_dialog(dialog)),
                MDRaisedButton(
                    text="Excluir", 
                    md_bg_color=(0.8, 0.2, 0.2, 1),
                    on_release=lambda x: self.delete_transacao(id_transacao, item_widget, dialog)
                )
            ]
        )
        dialog.open()
    
    def delete_transacao(self, id_transacao, item_widget, dialog):
        """Remove transação específica"""
        try:
            self.db.delete_transacao(id_transacao)
            self.close_dialog(dialog)
            
            if item_widget and hasattr(item_widget, 'parent') and item_widget.parent:
                item_widget.parent.remove_widget(item_widget)
            
            self.update_dashboard()
            self.update_transacoes_list()
            self.update_poupancas_list()
            
            self.show_message("Sucesso", "Transação removida!")
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            traceback.print_exc()
    
    def toggle_high_contrast(self, active):
        if active:
            self.theme_cls.primary_palette = "Yellow"
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"
    
    def go_to_config(self):
        self.root.current = 'config'
    
    def go_to_transacoes(self):
        self.update_transacoes_list()
        self.root.current = 'transacoes'
    
    def go_back(self):
        if self.root.current == 'config':
            self.update_dashboard()
        self.root.current = 'dashboard'
    
    def on_stop(self):
        try:
            self.db.close()
        except:
            pass

if __name__ == '__main__':
    FingestApp().run()