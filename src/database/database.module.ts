import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { DatabaseController } from './database.controller';
import { DatabaseService } from './database.service';

@Module({
  imports: [TypeOrmModule.forFeature([])],
  controllers: [DatabaseController],
  providers: [DatabaseService],
})
export class DatabaseModule {}
