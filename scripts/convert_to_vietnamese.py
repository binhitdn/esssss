#!/usr/bin/env python3
"""
Script to convert Portuguese (pt_BR) translations to Vietnamese template.
This creates a base Vietnamese translation that needs manual review.
"""
import re
import os
from pathlib import Path

# Translation mapping for common Portuguese -> Vietnamese
TRANSLATIONS = {
    # Headers
    'Portuguese (Brazil)': 'Vietnamese',
    'pt_BR': 'vi',
    'Português': 'Tiếng Việt',
    
    # Common UI terms
    'Configuração': 'Cấu Hình',
    'Configurar': 'Cấu Hình',
    'Painel': 'Bảng',
    'Canal': 'Kênh',
    'Servidor': 'Server',
    'Idioma': 'Ngôn Ngữ',
    'Temporizador': 'Bộ Đếm Thời Gian',
    'Pomodoro': 'Pomodoro',
    'Foco': 'Tập Trung',
    'Pausa': 'Nghỉ',
    'Descanso': 'Nghỉ Ngơi',
    'Notificação': 'Thông Báo',
    'Notificações': 'Thông Báo',
    'Membro': 'Thành Viên',
    'Membros': 'Thành Viên',
    'Permissão': 'Quyền',
    'Permissões': 'Quyền',
    'Administrador': 'Quản Trị Viên',
    'Gerenciar': 'Quản Lý',
    'Criar': 'Tạo',
    'Editar': 'Chỉnh Sửa',
    'Remover': 'Xóa',
    'Ativar': 'Bật',
    'Desativar': 'Tắt',
    'Ativado': 'Đã Bật',
    'Desativado': 'Đã Tắt',
    'Sucesso': 'Thành Công',
    'Erro': 'Lỗi',
    'Atenção': 'Chú Ý',
    'Obrigado': 'Cảm Ơn',
    'Por favor': 'Vui lòng',
    'Sim': 'Có',
    'Não': 'Không',
    'Você': 'Bạn',
    'Eu': 'Tôi',
    'Nós': 'Chúng tôi',
    
    # Time related
    'minuto': 'phút',
    'minutos': 'phút',
    'hora': 'giờ',
    'horas': 'giờ',
    'dia': 'ngày',
    'dias': 'ngày',
    'semana': 'tuần',
    'semanas': 'tuần',
    'mês': 'tháng',
    'meses': 'tháng',
    
    # Months
    'Janeiro': 'Tháng Một',
    'Fevereiro': 'Tháng Hai',
    'Março': 'Tháng Ba',
    'Abril': 'Tháng Tư',
    'Maio': 'Tháng Năm',
    'Junho': 'Tháng Sáu',
    'Julho': 'Tháng Bảy',
    'Agosto': 'Tháng Tám',
    'Setembro': 'Tháng Chín',
    'Outubro': 'Tháng Mười',
    'Novembro': 'Tháng Mười Một',
    'Dezembro': 'Tháng Mười Hai',
}

def update_header(content):
    """Update file header to Vietnamese"""
    # Update language team
    content = re.sub(
        r'"Language-Team: Portuguese \(Brazil\).*?"',
        '"Language-Team: Vietnamese"',
        content
    )
    
    # Update language code
    content = re.sub(
        r'"Language: pt_BR\\n"',
        '"Language: vi\\n"',
        content
    )
    
    # Update plural forms (Vietnamese has simpler plural rules)
    content = re.sub(
        r'"Plural-Forms:.*?\\n"',
        '"Plural-Forms: nplurals=1; plural=0;\\n"',
        content
    )
    
    # Update translator info
    content = re.sub(
        r'Last-Translator:.*',
        'Last-Translator: 14 hours a days, 2024',
        content
    )
    
    # Update revision date
    content = re.sub(
        r'"PO-Revision-Date:.*?"',
        '"PO-Revision-Date: 2024-12-17 06:53+0900\\n"',
        content
    )
    
    return content

def translate_content(content):
    """Apply basic translations"""
    for pt, vi in TRANSLATIONS.items():
        # Only replace in msgstr lines, not msgid
        content = re.sub(
            rf'(msgstr\s+"[^"]*){re.escape(pt)}([^"]*")',
            rf'\1{vi}\2',
            content,
            flags=re.IGNORECASE
        )
    
    return content

def process_file(filepath):
    """Process a single .po file"""
    print(f"Processing {filepath.name}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update header
    content = update_header(content)
    
    # Apply translations
    content = translate_content(content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Updated {filepath.name}")

def main():
    vi_dir = Path('locales/vi/LC_MESSAGES')
    
    if not vi_dir.exists():
        print(f"Error: {vi_dir} does not exist!")
        return 1
    
    # Skip babel.po as it's already manually translated
    po_files = [f for f in vi_dir.glob('*.po') if f.name != 'babel.po']
    
    print(f"Found {len(po_files)} .po files to process (excluding babel.po)")
    print("=" * 60)
    
    for po_file in sorted(po_files):
        try:
            process_file(po_file)
        except Exception as e:
            print(f"  ✗ Error processing {po_file.name}: {e}")
    
    print("=" * 60)
    print(f"✓ Processed {len(po_files)} files")
    print("\nNote: These are automatic translations and need manual review!")
    print("Many translations are still in Portuguese and need to be updated.")
    
    return 0

if __name__ == '__main__':
    exit(main())
