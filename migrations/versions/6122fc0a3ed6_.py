"""empty message

Revision ID: 6122fc0a3ed6
Revises: 
Create Date: 2022-08-06 20:57:21.065793

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6122fc0a3ed6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pet_score')
    op.alter_column('pet_apply_list', 'is_apply',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('pet_apply_list', 'is_apply',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    op.create_table('pet_score',
    sa.Column('馬爾濟斯', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('鬆獅犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('柯基', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('高山犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('貴賓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('柴犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('博美', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('秋田', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('法鬥', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('惡霸', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('雪納瑞', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('查理士', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('迷你品', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('哈士奇', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('吉娃娃', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('台灣犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('狐狸犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('臘腸', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('西施', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('大麥町', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('拉布拉多', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('米格魯', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('土狗', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('比特犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('阿富汗', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('狼犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('敖犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('傑克羅素', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('黃金獵犬', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('混種狗', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('金吉拉', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('美短毛貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('美短曼斥肯', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('豹貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('喜瑪拉雅貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('英國短毛貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('異國短毛貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('混種貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('俄羅斯藍貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('英國藍貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('緬因', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('加菲貓', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('波斯', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
